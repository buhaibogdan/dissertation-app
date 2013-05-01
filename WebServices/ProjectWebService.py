import sys
sys.path.append('/home/bb/PycharmProjects/dissertation-app')

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from Services.Project.ProjectService import ProjectService

from Services.Task.TaskService import TaskService

from tornado.options import define, options
from Services.UserProject.UserProjectService import UserProjectService
define("port", default=8001, help="run on the given port", type=int)

projectService = ProjectService(TaskService())
userProjectService = UserProjectService()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexHandler),
                    (r"/id", OneProject),
                    (r"/(\d+)/involvement", UsersInvolvedHandler)]
        settings = dict(debug=True)

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    """
    Projects handler - returns json of all projects
    """
    def get(self):
        self.set_header('content-type', 'application/json')
        projects = projectService.getProjects()
        p = []
        for project in projects:
            p.append({'pid': project.pid,
                      'title': project.title,
                      'description': project.description,
                      'owner': project.owner.username,
                      'release_date': project.release_date})

        self.write(json.dumps(p))


class UsersInvolvedHandler(tornado.web.RequestHandler):
    """
        Gets users involved in a project. Using project id - pid
    """
    def get(self, pid):
        usersInvolved = userProjectService.getUsersForProject(pid)
        u_list = []
        for user in usersInvolved:
            u_list.append({
                'username': user.users.username,
                'uid': user.uid
            })
        self.write(json.dumps(u_list))


class OneProject(tornado.web.RequestHandler):
    """
    Returns just one project. By project id (pid)
    """
    def get(self):
        pass


if __name__ == "__main__":

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()