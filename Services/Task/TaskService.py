from TaskDAO import TaskDAO

class TaskService(object):
    def __init__(self, dao):
        self.__DAO = dao

    def getTasksForProject(self, pid):
        return self.__DAO.getTasksForProject(pid)

    def getTask(self, id):
        return self.__DAO.getTask(id)

    def getTasksByUser(self, id):
        return self.__DAO.getTaskByUser(id)

    def getTasksAssignedTo(self, id):
        return self.__DAO.getTasksAssignedTo(id)