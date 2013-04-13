from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class User(Base):
    __tablename__ = 'User'
    uid = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(100))
    email = Column(String(100))
    last_connect = Column(DateTime())

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return 'User(%r) %r' % (self.uid, self.name)