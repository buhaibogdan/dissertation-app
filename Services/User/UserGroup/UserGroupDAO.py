from UserGroupEntity import UserGroupEntity
from Services.Database.db import db_session
from sqlalchemy.exc import SQLAlchemyError
from Services.Log.LogService import logService


class UserGroupDAO(object):
    def __init__(self):
        pass

    def getGroupsForUser(self, uid):
        userGroups = db_session.query(UserGroupEntity).filter(UserGroupEntity.uid == uid).all()
        groups = []

        for userGroup in userGroups:
            try:
                groups.append(userGroup.group.name)
            except SQLAlchemyError:
                logService.log_error('[SQL] Could not get group name for user in UserGroupDAO.')

        return groups