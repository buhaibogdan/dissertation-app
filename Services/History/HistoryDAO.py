from HistoryEntity import HistoryEntity
from Services.Database.db import db_session


class HistoryDAO(object):

    def __init__(self):
        pass

    def getHistory(self):
        return db_session.query(HistoryEntity).all()

    def getUserHistory(self, uid):
        return db_session.query(HistoryEntity).filter(HistoryEntity.uid == uid).all()

    def getProjectHistory(self, pid):
        return db_session.query(HistoryEntity).filter(HistoryEntity.pid == pid).all()

    def updateHistory(self, hEvent):
        db_session.add(hEvent)
        db_session.commit()

