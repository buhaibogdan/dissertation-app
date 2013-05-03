from Services.Database.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Services.Task import TaskEntity


class UserTaskEntity(Base):
    __tablename__ = 'user_task'
    user_id = Column(Integer, ForeignKey('user.uid'), primary_key=True)
    users = relationship('UserEntity')
    task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    tasks = relationship('TaskEntity')

    def __init__(self, user_id, task_id):
        self.user_id = user_id
        self.task_id = task_id