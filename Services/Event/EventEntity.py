from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class EventEntity(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Event: %r' % (self.uid, self.name)