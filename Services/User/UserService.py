# just to init the DB with SQLALCHEMY
from UserEntity import UserEntity
from UserPreferenceEntity import UserPreferenceEntity
from GroupPermision.GroupPermissionDAO import GroupPermissionDAO
from UserGroup.UserGroupDAO import UserGroupDAO
from Group.GroupDAO import GroupDAO
# end init
import json
from Services.Log.LogService import logService
import datetime


class UserService(object):

    @property
    def userGroupDAO(self):
        return UserGroupDAO()

    @property
    def groupPermission(self):
        return GroupPermissionDAO()

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

    def getUserGroups(self, uid):
        groups = self.userGroupDAO.getUserGroups(uid)
        group_list = []
        for group in groups:
            group_list.append(group.itervalues().next())
        return group_list

    def getPermissionsForUser(self, uid):
        groups = self.userGroupDAO.getUserGroups(uid)

        permissions = []
        for group in groups:
            group_id = group.iterkeys().next()
            group_permissions = self.groupPermission.getAllPermissionsForGroup(group_id)
            permissions.append(group_permissions)

        return permissions
