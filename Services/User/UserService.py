

class UserService(object):

    def __init__(self, userDAO):
        self.__DAO = userDAO

    def getUsers(self):
        return self.__DAO.getAllUsers()

    def getUserById(self, id):
        return self.__DAO.getUser(id)

    def getUserByUsername(self, username):
        return self.__DAO.getUserByUsername(username)
