from UserGroupEntity import UserGroupEntity
from Services.Database.db import db_session
from sqlalchemy.exc import SQLAlchemyError
from Services.Log.LogService import logService


class UserGroupDAO(object):
    def __init__(self, db=None):
        if not db:
            self._db = db_session

    def getUserGroups(self, uid):
        userGroups = self._db.query(UserGroupEntity).filter(UserGroupEntity.uid == uid).all()
        groups = []

        for userGroup in userGroups:
            try:
                groups.append({userGroup.group_id: userGroup.group.name})
            except SQLAlchemyError:
                logService.log_error('[SQL] Could not get group name for user in UserGroupDAO.')

        return groups