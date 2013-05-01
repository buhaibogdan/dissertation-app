from ProjectEntity import ProjectEntity
from Services.Database.db import DB, db_session, engine


class ProjectService(object):

    def __init__(self, taskService):
        self.taskService = taskService

    def getProjects(self):
        projects = db_session.query(ProjectEntity).all()

        for project in projects:
            project.release_date = str(project.release_date)
        return projects

    def getProject(self, id):
        project = db_session.query(ProjectEntity).filter(ProjectEntity.pid == id).first()
        return project

    def saveProject(self, newProject):
        pass