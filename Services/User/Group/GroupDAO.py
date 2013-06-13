from GroupEntity import GroupEntity
from Services.Database.db import db_session


class GroupDAO(object):
    def __init__(self, db=None):
        if not db:
            self._db = db_session
