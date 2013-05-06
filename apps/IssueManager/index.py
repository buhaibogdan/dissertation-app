from __builtin__ import property
import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.template
from Services.Database.db import *
import apps.IssueManager.ui_modules.modules
from sqlalchemy.exc import SQLAlchemyError
from Services.UserProject.UserProjectService import UserProjectService
from Services.Project.ProjectService import ProjectService
from Services.Project.ProjectDAO import ProjectDAO
from Services.User.UserDAO import UserDAO
from Services.User.UserService import UserService
from Services.UserTask.UserTaskService import UserTaskService
from Services.Task.TaskService import TaskService
from Services.Task.TaskDAO import TaskDAO
from ui_modules.modules import UserLinkModule
from Services.Log.LogService import LogService

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/projects", ProjectsHandler),
                    (r"/project/(\d+)", ProjectHandler),
                    (r"/issues", IssueHandler),
                    (r"/reports", ReportHandler)]
        settings = dict(template_path = os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"),
                        debug=True,
                        ui_modules=apps.IssueManager.ui_modules.modules,
                        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
                        xsrf_cookies=True,
                        login_url="/login"
        )

        tornado.web.Application.__init__(self, handlers, **settings)


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

    def get_current_user(self):
        return self.get_secure_cookie("username")


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html", username=self.get_current_user())

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." %status_code)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        userService = UserService(UserDAO())
        if userService.checkCredentials(username, password):
            self.set_secure_cookie("username", username)
            self.redirect("/")
        else:
            self.redirect('/login')

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." %status_code)


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
                    username=self.get_current_user())

    @tornado.web.authenticated
    def put(self):
        pid = self.get_argument('project_id', None)
        pTitle = self.get_argument('project_title', '')
        pOwnerId = self.get_argument('project_owner', None)
        pDescription = self.get_argument('project_description', '')
        pRelease = self.get_argument('project_release', None)
        sendEmail = self.get_argument('project_send_email', False) #TODO: handle this
        try:
            self.projectService.insertOrUpdateProject(pid, pTitle, pDescription, pOwnerId, pRelease)
            self.set_status(201)
        except SQLAlchemyError as err:
            self.logService.log_error("SQLAlchemyError while saving project: " + err.message)
            self.set_status(500)


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


class IssueHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        projects = self.projectService.getProjects()
        pid = self.get_argument('pid', projects[0].pid)
        tasksToDo = self.taskService.getTasksToDoForProject(pid)
        tasksInProgress = self.taskService.getTasksInProgressForProject(pid)
        tasksClosed = self.taskService.getTasksClosedForProject(pid)

        self.render("issues.html",
                    username=self.get_current_user(),
                    tasksToDo=tasksToDo,
                    tasksInProgress=tasksInProgress,
                    tasksClosed=tasksClosed,
                    projects=projects)


class ReportHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("reports.html", username=self.get_current_user())


if __name__ == "__main__":
    DB.init()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()