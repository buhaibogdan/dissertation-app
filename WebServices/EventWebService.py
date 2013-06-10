import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from Services.UserProject.UserProjectService import UserProjectService
from Services.Project.ProjectService import ProjectService
from Services.User.UserService import UserService
from Services.Project.ProjectDAO import ProjectDAO
from Services.User.UserDAO import UserDAO
from tornado.options import define, options
from Services.History.HistoryService import HistoryService
define("port", default=8001, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexHandler),
                    (r"/user/(\d+)", UserEvent),
                    (r"/project/(\d+)", ProjectEvent)]
        settings = dict(debug=True)

        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def historyService(self):
        return HistoryService()


class IndexHandler(BaseHandler):
    def get(self):
        allHistory = self.historyService.getHistory()
        self.write(self.historyService.convertToJson(allHistory))


class UserEvent(BaseHandler):
    def get(self, uid):
        userHistory = self.historyService.getUserHistory(uid)
        self.write(self.historyService.convertToJson(userHistory))


class ProjectEvent(BaseHandler):
    def get(self, pid):
        projectHistory = self.historyService.getProjectHistory(pid)
        self.write(self.historyService.convertToJson(projectHistory))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()