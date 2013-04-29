from UserProjectEntity import UserProjectEntity
from Services.Database.db import DB, db_session, engine
from Services.Project.ProjectEntity import ProjectEntity
import json

class UserProjectService(object):

    def __init__(self):
        pass

    '''
        Returns all projects in which a user is involved.
    '''
    def getProjectsForUser(self, uid):
        projects = db_session.query(UserProjectEntity).filter(uid=uid).all()
        projects_list = []
        for project in projects:
            projects_list.append(project.pid)

        return json.dumps(projects_list)
    '''
        Returns all users that are involved in a project.
    '''
    def getUsersForProject(self, pid):
        users = db_session.query(UserProjectEntity).filter( UserProjectEntity.pid == pid ).all()
        users_list = []
        for user in users:
            users_list.append({'uid':user.uid,
                               'username':user.users.username})

        return json.dumps(users_list)