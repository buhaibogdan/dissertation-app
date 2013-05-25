from __builtin__ import property
import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.template

import apps.IssueManager.ui_modules.modules
from Services.Log.LogService import logService

from tornado.options import define, options


define("port", default=7999, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexHandler)]
        settings = dict(template_path = os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"),
                        debug=True,
                        ui_modules=apps.IssueManager.ui_modules.modules,
                        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=", #TODO: generate key
                        xsrf_cookies=True,
                        login_url="/login"
                        )

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        errors = logService.getErrors()
        warnings = logService.getWarnings()
        notices = logService.getNotices()
        self.render("index.html", errors=errors, warnings=warnings, notices=notices)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()