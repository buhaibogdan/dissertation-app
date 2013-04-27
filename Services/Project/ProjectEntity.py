from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class ProjectEntity(Base):
    __tablename__ = 'Project'
    pid = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(600))
    id_owner = Column(Integer, primary_key=True)
    release_date = Column(DateTime)

    def __init__(self, title, description, id_owner):
        self.title = title
        self.description = description
        self.id_owner = id_owner

    def __repr__(self):
        return 'Project: %r' % (self.title)