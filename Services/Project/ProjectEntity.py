from Services.Database.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Services.User.UserEntity import UserEntity

class ProjectEntity(Base):
    __tablename__ = 'project'
    pid = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(600))
    id_owner = Column(Integer, ForeignKey('user.uid'))
    owner = relationship('UserEntity')
    release_date = Column(Date)

    def __init__(self, title, description, id_owner, release_date):
        self.title = title
        self.description = description
        self.id_owner = id_owner
        self.release_date = release_date

def __repr__(self):
        return 'Project: %r' % (self.title)