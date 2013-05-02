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

from Services.UserProject.UserProjectService import UserProjectService
from Services.Project.ProjectService import ProjectService
from Services.Project.ProjectDAO import ProjectDAO
from Services.User.UserDAO import UserDAO
from Services.User.UserService import UserService

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/projects", ProjectHandler),
                    (r"/issues", IssueHandler),
                    (r"/reports", ReportHandler)]
        settings = dict(template_path = os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"),
                        debug = True,
                        ui_modules=apps.IssueManager.ui_modules.modules)

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." %status_code)


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self, *args, **kwargs):
        #do some checks and redirect
        pass

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." %status_code)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/login");


class ProjectHandler(tornado.web.RequestHandler):
    def get(self):

        projectsService = ProjectService(ProjectDAO())
        userProjectService = UserProjectService()
        userService = UserService(UserDAO())

        projects = projectsService.getProjects()
        users = userService.getUsers()
        usersInvolved = userProjectService.getUsersForProject(1)

        self.render("projects.html", projects=projects, users=users, usersInvolved=usersInvolved)


class IssueHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("issues.html")


class ReportHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("reports.html")


if __name__ == "__main__":
    DB.init()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()