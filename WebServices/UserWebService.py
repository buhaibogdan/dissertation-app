import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json

from Services.User.UserService import UserService
from tornado.options import define, options

define("port", default=8002, help="run on the given port", type=int)

userService = UserService()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexHandler),
                    (r"/id", OneProject)]
        settings = dict(debug=True)

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    """
    Users handler - returns json of all users
    """
    def get(self):
        self.write("this is a test")


class OneProject(tornado.web.RequestHandler):
    """
    Returns just one user. By project id (uid)
    """
    def get(self):
        self.set_header('content-type', 'application/json')
        pass


if __name__ == "__main__":

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()