from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Services.User.Group.GroupEntity import GroupEntity
from Services.User.Permission.PermissionEntity import PermissionEntity
from Services.User.UserEntity import UserEntity


class UserGroupEntity(Base):
    __tablename__ = 'user_group'
    uid = Column(Integer, ForeignKey('user.uid'), primary_key=True)
    user = relationship('UserEntity')
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    group = relationship('GroupEntity')

    def __init__(self, uid, group_id):
        self.uid = uid
        self.group_id = group_id