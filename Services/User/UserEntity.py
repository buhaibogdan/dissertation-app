from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class UserEntity(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(100))
    email = Column(String(100))
    last_connect = Column(DateTime())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return 'User(%r) %r' % (self.uid, self.username)