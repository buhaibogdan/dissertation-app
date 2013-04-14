import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import random
import tornado.template
from Services.Database.db import DB

from Services.Alert import AlertEntity
from Services.Project import ProjectEntity
from Services.Task import TaskEntity
from Services.User import UserEntity


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexHandler),
            (r"/(\w+)", HelloHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler)]
        settings = dict(template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug = True)

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", name = "Bogdan")

    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." %status_code)


class HelloHandler(tornado.web.RequestHandler):
    def get(self, name):
        self.write('Hello %r', name)


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

if __name__ == "__main__":
    DB.init()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()