from Services.Database.db import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from PreferenceEntity import PreferenceEntity


class UserPreferenceEntity(Base):
    __tablename__ = 'user_preference'
    uid = Column(Integer, ForeignKey('user.uid'), primary_key=True)
    user = relationship('UserEntity')
    preference_id = Column(Integer, ForeignKey('preference.id'), primary_key=True)
    preference = relationship('PreferenceEntity')
    active = Column(Boolean, nullable=False, default=False)

    def __init__(self, uid, preference_id, active):
        self.uid = uid
        self.preference_id = preference_id
        self.active = active