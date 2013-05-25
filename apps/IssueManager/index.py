from __builtin__ import property
import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.template
from Handlers import AsyncHandlers
from Handlers import SyncHandleres

from Services.Database.db import *
import apps.IssueManager.ui_modules.modules


from tornado.options import define, options


define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/",                          SyncHandleres.IndexHandler),
                    (r"/login",                     SyncHandleres.LoginHandler),
                    (r"/logout",                    SyncHandleres.LogoutHandler),
                    (r"/projects",                  SyncHandleres.ProjectsHandler),
                    (r"/project/(\d+)",             SyncHandleres.ProjectHandler),
                    (r"/project/(\d+)/issues",      SyncHandleres.IssuesHandler),
                    (r"/issues",                    SyncHandleres.IssuesHandler),
                    (r"/issue/(\d+)",               SyncHandleres.IssueHandler),
                    (r"/issue/(\d+)?_xsrf=(\w+)",   SyncHandleres.IssueHandler),
                    (r"/issue/(\d+)/time",          SyncHandleres.IssueHandler),
                    (r"/history",                   AsyncHandlers.HistoryHandler),
                    (r"/history/user/(\d+)",        AsyncHandlers.UserHistoryHandler),
                    (r"/history/project/(\d+)",     AsyncHandlers.ProjectHistoryHandler),
                    (r"/users$",                    SyncHandleres.UserHandler),
                    (r"/users/(\d+)",               SyncHandleres.UserHandler),
                    (r"/reports",                   SyncHandleres.ReportHandler)]
        settings = dict(template_path = os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"),
                        debug=True,
                        ui_modules=apps.IssueManager.ui_modules.modules,
                        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=", #TODO: generate key
                        xsrf_cookies=True,
                        login_url="/login"
                        )

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    DB.init()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()