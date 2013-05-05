from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Services.Project.ProjectEntity import ProjectEntity
from Services.User.UserEntity import UserEntity


class TaskEntity(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(600))
    assignee_id = Column(Integer, ForeignKey('user.uid'))
    assignee = relationship('UserEntity', primaryjoin="TaskEntity.assignee_id==UserEntity.uid")
    reporter_id = Column(Integer, ForeignKey('user.uid'))
    reporter = relationship('UserEntity', primaryjoin="TaskEntity.reporter_id==UserEntity.uid")
    project_id = Column(Integer, ForeignKey('project.pid'))
    project = relationship('ProjectEntity')
    minutes_estimated = Column(Integer)
    minutes_remaining = Column(Integer)
    priority = Column(String(40))
    complexity = Column(Integer)


    def __init__(self, title, description, id_assignee, id_reporter, id_project, minutes_estimated, minutes_remaining, complexity, priority):
        self.title = title
        self.description = description
        self.assignee_id = id_assignee
        self.reporter_id = id_reporter
        self.project_id = id_project
        self.minutes_estimated = minutes_estimated
        self.minutes_remaining = minutes_remaining
        self.complexity = complexity
        self.priority = priority
        self.complexity = complexity

    def __repr__(self):
        return 'Task %r' % self.name