import requests
import tornado.web

from apps.IssueManager.ui_modules.modules import UserLinkModule
from sqlalchemy.exc import SQLAlchemyError
from Services.UserProject.UserProjectService import UserProjectService
from Services.Project.ProjectService import ProjectService
from Services.Project.ProjectDAO import ProjectDAO
from Services.User.UserDAO import UserDAO
from Services.User.UserService import UserService
from Services.UserTask.UserTaskService import UserTaskService
from Services.Task.TaskService import TaskService
from Services.Task.TaskDAO import TaskDAO
from Services.Log.LogService import LogService
from Services.Task.TaskEntity import TaskEntity
from Services.History.HistoryService import HistoryService
from Services.Event.EventService import EventService


class BaseHandler(tornado.web.RequestHandler):
    """ This is lazy initialization
    """
    @property
    def userService(self):
        return UserService(UserDAO())

    @property
    def projectService(self):
        return ProjectService(ProjectDAO())

    @property
    def userProjectService(self):
        return UserProjectService()

    @property
    def taskService(self):
        return TaskService(TaskDAO())

    @property
    def userTaskService(self):
        return UserTaskService()

    @property
    def logService(self):
        return LogService()

    @property
    def historyService(self):
        return HistoryService()
    @property
    def eventService(self):
        return EventService()

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_current_user_id(self):
        return self.get_secure_cookie('uid')

    def check_xsrf_cookie(self):
        _xsrf = self.get_argument('_xsrf', 'ciuciu')
        return True


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
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
        user = self.userService.checkCredentials(username, password)
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
        projects = self.projectService.getProjects()
        users = self.userService.getUsers()
        usersInvolved = self.userProjectService.getUsersForProject(1)

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
        try:
            self.projectService.insertOrUpdateProject(pid, pTitle, pDescription, pOwnerId, pRelease)
            self.set_status(201)
        except SQLAlchemyError as err:
            self.logService.log_error("SQLAlchemyError while saving project: " + err.message)
            self.set_status(500)

        #update history
        #self.historyService.updateHistory()
            #send out emails
        if notify:
            self.historyService.sendEmails(self.get_current_user_id(), pid, self.get_current_user()
                                           + " created a new task.")


class ProjectHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, pid):
        project = self.projectService.getProjectAsJson(pid)
        peopleInvolved = self.userProjectService.getUsersForProject(pid)
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
        projects = self.projectService.getProjects()
        # use first project if no parameter pid is passed
        pid = self.get_argument('pid', projects[0].pid) if pid is None else pid
        tasksToDo = self.taskService.getTasksToDoForProject(pid)
        tasksInProgress = self.taskService.getTasksInProgressForProject(pid)
        tasksDone = self.taskService.getTasksClosedForProject(pid)
        usersInProject = self.userProjectService.getUsersForProject(pid)

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
        result = self.taskService.insertOrUpdateTask(task)
        if result is False:
            self.set_status(500)
        self.set_status(201)

        #update history
        self.historyService.updateHistory(
            self.get_current_user_id(),
            pid,
            self.eventService.getEventByName(EventService.create_task).id,
            self.get_current_user() + ' created task with title '
            + title + ' for project ' + self.projectService.getProject(pid).title
        )
        #send out emails
        if notify:
            self.historyService.sendEmails(self.get_current_user_id(), pid, self.get_current_user()
                                           + " created a new task.")


class IssueHandler(BaseHandler):
    """
        Handle issues removal and editing.
    """
    @tornado.web.authenticated
    def delete(self, task_id):
        try:
            self.taskService.deleteTask(task_id)
        except SQLAlchemyError as err:
            raise err

    @tornado.web.authenticated
    def put(self, task_id):
        status = self.get_argument('status')
        #update history
        pid = self.get_argument('pid')
        self.taskService.updateTaskStatus(task_id, status)
        message = self.get_current_user() \
            + " updated task " \
            + self.taskService.getTask(task_id).title \
            + " from project " \
            + self.projectService.getProject(pid).title

        self.historyService.updateHistory(
            self.get_current_user_id(),
            pid,
            self.eventService.getEventByName(EventService.update_task).id,
            message
        )



class ReportHandler(BaseHandler):
    """
        Handle reports and stuff.
    """
    @tornado.web.authenticated
    def get(self):
        self.render("reports.html",
                    username=self.get_current_user(),
                    uid=self.get_current_user_id())

