from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Services.Project.ProjectEntity import ProjectEntity
from Services.User.UserEntity import UserEntity
from StatusEntity import StatusEntity
from sqlalchemy.ext.hybrid import hybrid_property
from Services.Utils.TimeConvertService import TimeConvertService

class TaskEntity(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(600))
    assignee_id = Column(Integer, ForeignKey('user.uid'), nullable=False)
    assignee = relationship('UserEntity', primaryjoin="TaskEntity.assignee_id==UserEntity.uid")
    reporter_id = Column(Integer, ForeignKey('user.uid'), nullable=False)
    reporter = relationship('UserEntity', primaryjoin="TaskEntity.reporter_id==UserEntity.uid")
    project_id = Column(Integer, ForeignKey('project.pid'), nullable=False)
    project = relationship('ProjectEntity')
    _minutes_estimated = Column("minutes_estimated", Integer)
    _minutes_remaining = Column("minutes_remaining", Integer)
    priority = Column(String(40))
    complexity = Column(Integer)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False, default=1)
    status = relationship('StatusEntity')

    def __init__(self, title, description, id_assignee, id_reporter, id_project, minutes_estimated, complexity, priority):
        self.title = title
        self.description = description
        self.assignee_id = id_assignee
        self.reporter_id = id_reporter
        self.project_id = id_project
        self.minutes_estimated = minutes_estimated
        self.complexity = complexity
        self.priority = priority
        self.complexity = complexity

    def __repr__(self):
        return 'Task %r' % self.name

    @hybrid_property
    def minutes_estimated(self):
        return TimeConvertService.convertFromMinutes(self._minutes_estimated)

    @minutes_estimated.setter
    def minutes_estimated(self, minutes_estimated):
        self._minutes_estimated = TimeConvertService.convertToMinutes(minutes_estimated)

    @hybrid_property
    def minutes_remaining(self):
        return TimeConvertService.convertFromMinutes(self._minutes_remaining)

    @minutes_estimated.setter
    def minutes_estimated(self, minutes_remaining):
        self._minutes_remaining = TimeConvertService.convertToMinutes(minutes_remaining)