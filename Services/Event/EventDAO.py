from EventEntity import EventEntity
from Services.Database.db import db_session


class EventDAO(object):
    def __init__(self):
        pass

    def getEvents(self):
        return db_session.query(EventEntity).all()

    def getEventByName(self, name):
        return db_session.query(EventEntity).filter(EventEntity.name == name).first()