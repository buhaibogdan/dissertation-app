from Services.Database.db import Base
from sqlalchemy import Column, Integer, String


class PermissionEntity(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    codename = Column(String(20), nullable=True)

    def __init__(self, id, name, codename):
        self.id = id
        self.name = name
        self.codename = codename