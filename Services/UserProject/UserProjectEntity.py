from Services.Database.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Services.Project.ProjectEntity import ProjectEntity

class UserProjectEntity(Base):
    __tablename__ = 'user_project'
    uid = Column(Integer, ForeignKey('user.uid'), primary_key=True)
    users = relationship('UserEntity')
    pid = Column(Integer, ForeignKey('project.pid'), primary_key=True)
    projects = relationship('ProjectEntity')

    def __init__(self, uid, pid):
        self.uid = uid
        self.pid = pid