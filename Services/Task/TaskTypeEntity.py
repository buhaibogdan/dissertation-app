from Services.Database.db import Base
from sqlalchemy import Column, Integer, String


class TaskTypeEntity(Base):
    __tablename__ = 'task_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'TaskType %r' % self.name