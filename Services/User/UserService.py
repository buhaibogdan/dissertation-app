from UserEntity import UserEntity
from UserPreferenceEntity import UserPreferenceEntity
import json
from Services.Log.LogService import logService
import datetime


class UserService(object):

    def __init__(self, userDAO):
        self.__DAO = userDAO

    def getUsers(self):
        return self.__DAO.getAllUsers()

    def getUserById(self, id):
        return self.__DAO.getUserById(id)

    def getUserByUsername(self, username):
        return self.__DAO.getUserByUsername(username)

    def checkCredentials(self, username, password):
        user = self.__DAO.getUserByUsername(username)
        if user.password != password:
            return False
        user.last_connect = datetime.datetime.now()
        return user

    def userToJson(self, user):
        try:
            userJson = {
                'uid': user.uid,
                'username': user.username,
                'email': user.email,
                'last_connect': str(user.last_connect)
            }
        except AttributeError:
            logService.log_error('UserService: Could not convert list of users to json.')
            userJson = {}
        return json.dumps(userJson)

    def usersToJson(self, users):
        usersJson = []
        try:
            for user in users:
                usersJson.append({
                    'uid': user.uid,
                    'username': user.username,
                    'email': user.email,
                    'last_connect': str(user.last_connect)
                })
        except AttributeError:
            #log error
            logService.log_error('UserService: Could not convert list of users to json.')
        return json.dumps(usersJson)
