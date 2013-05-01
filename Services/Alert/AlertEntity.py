from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class AlertEntity(Base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Alert: %r' % (self.uid, self.name)