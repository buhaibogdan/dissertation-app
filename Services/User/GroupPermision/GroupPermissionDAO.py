from GroupPermissionEntity import GroupPermissionEntity
from Services.Database.db import db_session
from sqlalchemy.exc import SQLAlchemyError
from Services.Log.LogService import logService


class GroupPermissionDAO(object):
    def __init__(self, db=None):
        if not db:
            self._db = db_session

    def getAllPermissionsForGroup(self, group_id):
        perms = self._db.query(GroupPermissionEntity).filter(GroupPermissionEntity.group_id == group_id).all()
        permissions = []
        for perm in perms:
            try:
                permissions.append(perm.permission.codename)
            except SQLAlchemyError:
                logService.log_error('[SQL] Could not get permission codename for group in GroupPermissionDAO')

        return permissions