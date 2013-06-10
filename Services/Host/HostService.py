from Services.UserProject.UserProjectService import UserProjectService
from Services.Project.ProjectService import ProjectService
from Services.Project.ProjectDAO import ProjectDAO
from Services.User.UserDAO import UserDAO
from Services.User.UserService import UserService
from Services.Task.TaskService import TaskService
from Services.Task.TaskDAO import TaskDAO
from Services.Log.LogService import logService
from Services.History.HistoryService import HistoryService
from Services.Event.EventService import EventService


class HostService(object):
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
    def logService(self):
        return logService

    @property
    def historyService(self):
        return HistoryService()

    @property
    def eventService(self):
        return EventService()


hostService = HostService()