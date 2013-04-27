from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String, length=40)
    order = Column(Integer)

    def __init__(self, name, order):
        self.name = name
        self.order = order

    def __repr__(self):
        return 'Status %r' % (self.name)