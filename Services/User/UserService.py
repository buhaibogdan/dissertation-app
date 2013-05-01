from UserEntity import UserEntity
from Services.Database.db import DB, db_session, engine


class UserService(object):

    def __init__(self):
        pass

    def getUsers(self):
        users = db_session.query(UserEntity).all()
        for user in users:
            user.last_connect = str(user.last_connect)
        return users

    def getUserById(self, id):
        pass

    def getUserByUsername(self, username):
        pass

    def saveProject(self, newProject):
        pass