from UserProjectEntity import UserProjectEntity
from Services.Database.db import db_session


class UserProjectService(object):

    def __init__(self):
        pass

    """
        Returns all projects in which a user is involved.
    """
    def getProjectsForUser(self, uid):
        projects = db_session.query(UserProjectEntity).filter(uid=uid).all()
        return projects
    """
        Returns all users that are involved in a project.
    """
    def getUsersForProject(self, pid):
        usersInvolved = db_session.query(UserProjectEntity).filter(UserProjectEntity.pid == pid).all()
        return usersInvolved