from Services.Database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Services.User.Group.GroupEntity import GroupEntity
from Services.User.Permission.PermissionEntity import PermissionEntity


class GroupPermissionEntity(Base):
    __tablename__ = 'group_permission'
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    group = relationship('GroupEntity')
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)
    permission = relationship('PermissionEntity')

    def __init__(self, group_id, permission_id):
        self.group_id = group_id
        self.permission_id = permission_id