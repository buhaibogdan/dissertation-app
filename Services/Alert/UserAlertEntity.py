from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class UserAlert(Base):
    __tablename__ = 'UserAlert'
    uid = Column(Integer, primary_key=True, autoincrement=False)
    alert_id = Column(Integer(50), primary_key=True, autoincrement=False)
    status = Column(Boolean, nullable=False)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return 'UserAlert(%r) %r' % (self.uid, self.name)