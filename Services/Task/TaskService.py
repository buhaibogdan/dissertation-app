from TaskDAO import TaskDAO
from sqlalchemy.exc import SQLAlchemyError
from Services.Utils.TimeConvertService import TimeConvertService
import re


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
        if "Done" in tasks.keys():
            return tasks['Done']
        return []

    def insertOrUpdateTask(self, task):
        try:
            id = self.__DAO.insertOrUpdateTask(task)
            return id
        except SQLAlchemyError:
            return False

    def deleteTask(self, id):
        return self.__DAO.deleteTask(id)

    def updateTaskStatus(self, id, status):
        self.__DAO.updateTaskStatus(id, status)

    def logTime(self, task_id, timeLogged, adjustBy=0):
        try:
            task = self.getTask(task_id)
            if adjustBy != 0:
                task.logTime(TimeConvertService.convertToMinutes(adjustBy))
            else:
                task.logTime(TimeConvertService.convertToMinutes(timeLogged))
            self.insertOrUpdateTask(task)
            return True
        except AttributeError:
            return False
        except SQLAlchemyError:
            return False