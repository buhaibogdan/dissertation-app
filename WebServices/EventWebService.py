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
import base64
from conf.conf import certs_ws, certs


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

    def get_current_user(self):
        auth_header = self.request.headers.get('Authorization')
        if auth_header is None:
            return self._request_auth_header()
        if not auth_header.startswith('Basic '):
            return self._request_auth_header()

        auth_decode = base64.decodestring(auth_header[6:])
        username, password = auth_decode.split(':', 2)

        if username == 'bb' and password == 'bb':
            return 'bb'
        raise tornado.web.HTTPError(403, 'Credentials are invalid.')

    def _request_auth_header(self):
        self.set_header('WWW-Authenticate', 'Basic realm=events')
        self.set_status(401)
        self.finish()
        return False


class IndexHandler(BaseHandler):

    def get(self):
        from Services.Log.LogService import logService
        self.get_current_user()
        allHistory = self.historyService.getHistory()
        self.write(self.historyService.convertToJson(allHistory))


class UserEvent(BaseHandler):
    def get(self, uid):
        self.get_current_user()
        userHistory = self.historyService.getUserHistory(uid)
        self.write(self.historyService.convertToJson(userHistory))


class ProjectEvent(BaseHandler):
    def get(self, pid):
        self.get_current_user()
        projectHistory = self.historyService.getProjectHistory(pid)
        self.write(self.historyService.convertToJson(projectHistory))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        Application(),
        ssl_options={"certfile": certs['certfile'],
                     "keyfile": certs['keyfile']})
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()