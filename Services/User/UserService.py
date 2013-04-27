from UserEntity import UserEntity
from Services.Database.db import DB, db_session, engine
import json

class UserService(object):

    def __init__(self):
        pass

    def getUsers(self):
        users = db_session.query(UserEntity).all()
        users_list = []
        for user in users:
            users_list.append({'uid':user.uid,
                          'username':user.username,
                          'email':user.email,
                          'last_connect':str(user.last_connect)})

        return json.dumps(users_list)

    def getUserById(self, id):
        pass

    def getUserByUsername(self, username):
        pass

    def saveProject(self, newProject):
        pass