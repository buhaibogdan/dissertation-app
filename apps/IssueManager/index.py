import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import random
import tornado.template
from Services.Database.db import *

import json
from Services.Alert import AlertEntity
from Services.Project import ProjectEntity
from Services.Task import TaskEntity
from Services.User import UserEntity


from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)


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
            debug = True)

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
        from Services.Project.ProjectService import ProjectService
        from Services.Task.TaskService import TaskService
        from Services.User.UserService import UserService

        projectService = ProjectService(TaskService())
        projects = json.loads(projectService.getProjects())

        userService = UserService()
        users = json.loads(userService.getUsers());
        self.render("projects.html", projects=projects, users = users);


class IssueHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("issues.html");


class ReportHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("reports.html");


if __name__ == "__main__":
    DB.init()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()