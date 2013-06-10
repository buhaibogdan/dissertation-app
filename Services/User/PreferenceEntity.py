from Services.Database.db import Base
from sqlalchemy import Column, Integer, String


class PreferenceEntity(Base):
    __tablename__ = 'preference'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, id, name):
        self.id = id
        self.name = name