from TaskEntity import TaskEntity
from Services.Database.db import db_session


class TaskDAO(object):
    def __init__(self):
        pass

    def getTasksForProject(self, pid):
        return db_session.query(TaskEntity).filter(TaskEntity.project_id == pid)

    def getTask(self, id):
        return db_session.query(TaskEntity).filter(TaskEntity.id == id).first()

    def getTasksByUser(self, id):
        return db_session.query(TaskEntity).filter(TaskEntity.reported_id == id)

    def getTasksAssignedTo(self, id):
        return db_session.query(TaskEntity).filter(TaskEntity.reported_id == id)

    def insertOrUpdateTask(self, task):
        db_session.add(task)
        db_session.commit()
        return task.id