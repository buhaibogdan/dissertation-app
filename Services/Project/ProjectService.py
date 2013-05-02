

class ProjectService(object):

    def __init__(self, projectDAO, taskService=None):
        self.taskService = taskService
        self.__DAO = projectDAO

    def getProjects(self):
        return self.__DAO.getAllProjects()

    def getProject(self, id):
        return self.__DAO.getProject(id)