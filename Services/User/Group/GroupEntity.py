from Services.Database.db import Base
from sqlalchemy import Column, Integer, String


class GroupEntity(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(60), nullable=True)

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description