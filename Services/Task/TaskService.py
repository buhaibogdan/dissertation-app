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

    def getTasksByStatusForProject(self, pid):
        tasks = self.getTasksForProject(pid)
        sortedTasks = {}
        for task in tasks:
            if task.status.name in sortedTasks.keys():
                sortedTasks[task.status.name].append(task)
            else:
                sortedTasks[task.status.name] = [task]
        return sortedTasks

    def getTasksToDoForProject(self, pid):
        tasks = self.getTasksByStatusForProject(pid)
        if "To Do" in tasks.keys():
            return tasks['To Do']
        return []

    def getTasksInProgressForProject(self, pid):
        tasks = self.getTasksByStatusForProject(pid)
        if "In Progress" in tasks.keys():
            return tasks['In Progress']
        return []

    def getTasksClosedForProject(self, pid):
        tasks = self.getTasksByStatusForProject(pid)
        if "Closed" in tasks.keys():
            return tasks['Closed']
        return []