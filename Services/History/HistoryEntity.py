from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Services.User.UserEntity import UserEntity
from Services.Project.ProjectEntity import ProjectEntity
from Services.Event.EventEntity import EventEntity


class HistoryEntity(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.uid'), nullable=False)
    user = relationship('UserEntity')
    pid = Column(Integer, ForeignKey('project.pid'))
    project = relationship('ProjectEntity')
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    event = relationship('EventEntity')
    message = Column(String(200), nullable=False)



    '''
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
    type_id = Column(Integer, ForeignKey('task_type.id'), nullable=False, default=1)
    type = relationship('TaskTypeEntity')'''

    def __init__(self, uid, pid, event_id, message):
        self.uid = uid
        self.pid = pid
        self.event_id = event_id
        self.message = message

    def __repr__(self):
        return 'History obj'