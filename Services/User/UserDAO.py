from UserEntity import UserEntity
from Services.Database.db import db_session


class UserDAO(object):

    def __init__(self):
        pass

    def getAllUsers(self):
        users = db_session.query(UserEntity).all()
        for user in users:
            user.last_connect = str(user.last_connect)
        return users

    def getUserById(self, id):
        user = db_session.query(UserEntity).filter(UserEntity.uid == id).first()
        return user

    def getUserByUsername(self, username):
        user = db_session.query(UserEntity).filter(UserEntity.username == username).first()
        return user
