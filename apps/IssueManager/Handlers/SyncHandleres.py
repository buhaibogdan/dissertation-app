import requests
import tornado.web

from apps.IssueManager.ui_modules.modules import UserLinkModule
from apps.IssueManager.ui_modules.modules import IssueLogWorkModule
from sqlalchemy.exc import SQLAlchemyError
from Services.Task.TaskEntity import TaskEntity
from Services.History.HistoryService import HistoryService
from Services.Event.EventService import EventService
from Services.Host.HostService import hostService
from Services.Report.ReportServiceClient import ReportServiceClient
from Services.Report.ReportService import ReportService


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_current_user_id(self):
        return self.get_secure_cookie('uid')

    def check_xsrf_cookie(self):
        _xsrf = self.get_argument('_xsrf', '')
        return True


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        from Services.Utils.EmailService import EmailService
        es = EmailService()
        #es.setTo("buhaibogdan@yahoo.com")
        #es.setBody("just some text for test here")
        #es.setSubject("Test")
        #es.send()
        self.render("index.html",
                    username=self.get_current_user(),
                    uid=self.get_current_user_id())

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." % status_code)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = hostService.userService.checkCredentials(username, password)
        if user is not False:
            self.set_secure_cookie("username", user.username)
            self.set_secure_cookie('uid', str(user.uid))
            self.redirect("/")
        else:
            self.redirect('/login')

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." % status_code)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.redirect('/login')


class ProjectsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        projects = hostService.projectService.getProjects()
        users = hostService.userService.getUsers()
        usersInvolved = hostService.userProjectService.getUsersForProject(1)

        self.render("projects.html",
                    projects=projects,
                    users=users,
                    usersInvolved=usersInvolved,
                    username=self.get_current_user(),
                    uid=self.get_current_user_id())

    @tornado.web.authenticated
    def put(self):
        pid = self.get_argument('project_id', None)
        pTitle = self.get_argument('project_title', '')
        pOwnerId = self.get_argument('project_owner', None)
        pDescription = self.get_argument('project_description', '')
        pRelease = self.get_argument('project_release', None)
        notify = self.get_argument('notify', False) #TODO: handle this
        if pid is None:
            message = self.get_current_user() + " created a new project: " + pTitle + "."
            eventId = hostService.eventService.getEventByName(hostService.eventService.add_project).id
        else:
            message = self.get_current_user() + " updated project " + pTitle + "."
            eventId = hostService.eventService.getEventByName(hostService.eventService.add_project).id
        try:
            pid = hostService.projectService.insertOrUpdateProject(pid, pTitle, pDescription, pOwnerId, pRelease)
            self.set_status(201)
        except SQLAlchemyError as err:
            hostService.logService.log_error("SQLAlchemyError while saving project: " + err.message)
            self.set_status(500)
            self.finish()

        #update history
        hostService.historyService.updateHistory(
            self.get_current_user_id(),
            pid,
            eventId,
            message
        )
        #send out emails
        if notify:
            hostService.historyService.sendEmails(self.get_current_user_id(), pid, self.get_current_user()
                                                                            + " created a new project: " + pTitle + ".")


class ProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, pid):
        project = hostService.projectService.getProjectAsJson(pid)
        peopleInvolved = hostService.userProjectService.getUsersForProject(pid)
        peopleInvolvedHtml = ''
        ui = UserLinkModule(self)

        for user in peopleInvolved:
            peopleInvolvedHtml += ui.render(user)
            if user != peopleInvolved[-1]:
                peopleInvolvedHtml += ", "

        project['people'] = peopleInvolvedHtml
        self.write(project)

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." % status_code)


class IssuesHandler(BaseHandler):
    """
        Handle issues for projects
    """

    @tornado.web.authenticated
    def get(self, pid=None):
        h = HistoryService()
        projects = hostService.projectService.getProjects()
        # use first project if no parameter pid is passed
        pid = self.get_argument('pid', projects[0].pid) if pid is None else pid
        tasksToDo = hostService.taskService.getTasksToDoForProject(pid)
        tasksInProgress = hostService.taskService.getTasksInProgressForProject(pid)
        tasksDone = hostService.taskService.getTasksClosedForProject(pid)
        usersInProject = hostService.userProjectService.getUsersForProject(pid)

        self.render("issues.html",
                    username=self.get_current_user(),
                    tasksToDo=tasksToDo,
                    tasksInProgress=tasksInProgress,
                    tasksDone=tasksDone,
                    projects=projects,
                    pid=pid,
                    usersInProject=usersInProject,
                    uid=self.get_current_user_id())

    @tornado.web.authenticated
    def post(self, pid):
        reporter_id = int(self.get_current_user_id())
        id = int(self.get_argument('task_id', 0))
        title = self.get_argument('title', None)
        description = self.get_argument('description', '')
        priority = int(self.get_argument('priority', 1))
        assignee_id = int(self.get_argument('assignee', reporter_id))
        complexity = self.get_argument('complexity', 0)
        estimate = self.get_argument('estimation', '')
        task_type = self.get_argument('type', 1)
        notify = self.get_argument('notify', False)
        task = TaskEntity(title, description, assignee_id, reporter_id, pid, estimate, complexity, priority, task_type)
        if id != 0:
            task.id = id
        result = hostService.taskService.insertOrUpdateTask(task)
        if result is False:
            self.set_status(500)
        self.set_status(201)

        #update history
        hostService.historyService.updateHistory(
            self.get_current_user_id(),
            pid,
            hostService.eventService.getEventByName(EventService.create_task).id,
            self.get_current_user() + ' created task with title '
            + title + ' for project ' + hostService.projectService.getProject(pid).title
        )
        #send out emails
        if notify:
            hostService.historyService.sendEmails(self.get_current_user_id(), pid, self.get_current_user()
                                                                            + " created a new task.")


class IssueHandler(BaseHandler):
    """
        Content for log work modal
    """

    @tornado.web.authenticated
    def get(self, id):
        task = hostService.taskService.getTask(id)
        module = IssueLogWorkModule(self)
        self.write(module.render(task))

    """
        Handle issues removal and editing.
    """

    @tornado.web.authenticated
    def delete(self, task_id):
        try:
            hostService.taskService.deleteTask(task_id)
        except SQLAlchemyError as err:
            raise err

    @tornado.web.authenticated
    def put(self, task_id):
        status = self.get_argument('status', None)
        pid = self.get_argument('pid')

        if status is not None:
            hostService.taskService.updateTaskStatus(task_id, status)
            self.set_status(200)
            #update history message
            message = self.get_current_user() \
                      + " updated task " \
                      + hostService.taskService.getTask(task_id).title \
                      + " from project " \
                      + hostService.projectService.getProject(pid).title
        else:
            timeLogged = self.get_argument('log_work_value', 0)
            if not timeLogged:
                self.set_status(400)
                self.finish()

            adjustBy = self.get_argument('log_work_adjust_by', 0)
            if hostService.taskService.logTime(task_id, timeLogged, adjustBy):
                self.set_status(200)
            else:
                self.set_status(500)
                #update history message
            message = self.get_current_user() \
                      + " logged " \
                      + timeLogged \
                      + " on task " \
                      + hostService.taskService.getTask(task_id).title \
                      + " from project " \
                      + hostService.projectService.getProject(pid).title

        hostService.historyService.updateHistory(
            self.get_current_user_id(),
            pid,
            hostService.eventService.getEventByName(EventService.update_task).id,
            message
        )


class UserHandler(BaseHandler):
    def get(self, uid=None):
        self.set_header('Content-Type', 'application/json')
        if uid:
            user = hostService.userService.getUserById(uid)
            response = hostService.userService.userToJson(user)
        else:
            users = hostService.userService.getUsers()
            response = hostService.userService.usersToJson(users)
        self.write(response)

    def put(self):
        pass

    def delete(self, uid):
        pass

    def post(self):
        pass


class ReportHandler(BaseHandler):
    """
        Handle reports and stuff.
    """

    #@tornado.web.authenticated
    def get(self):
        projects = hostService.projectService.getProjects()
        pid = self.get_argument('pid', 0)

        # speed test for scalability
        test = self.get_argument('test', None)
        case = self.get_argument('case', None)
        case1 = 0
        case2 = 0
        if test == 1 or test == '1':
            import time
            # case 1:
            # default
            start = time.time()

            for i in range(0, 20):
                s = ReportService()
                projectReport = s.createReportForProject(pid)
            finish = time.time()
            case1 = finish-start

            # case 2:
            # rabbitmq with n workers
            start = time.time()
            for i in range(0, 20):
                reportServiceClient = ReportServiceClient()
                projectReport = reportServiceClient.call_generate_project_report(pid)
            finish = time.time()
            case2 = finish - start

        # case 1 mai rapid decat case 2
        # to note this
        # also test with siege :D

        # user amqp to generate pdf => alert user pdf is ready or send it to his email (might be better)

        #reportServiceClient = ReportServiceClient()
        #projectReport = reportServiceClient.call_generate_project_report(pid)
        s = ReportService()
        #projectReport = s.createReportForProject(pid)
        s.createReportForProjectPDF(pid)

        self.render("reports.html",
                    username=self.get_current_user(),
                    uid=self.get_current_user_id(),
                    projects=projects,
                    pid=pid,
                    projectReport=1,
                    case1=case1,
                    case2=case2)

