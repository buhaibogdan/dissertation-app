from ProjectEntity import ProjectEntity
from Services.Database.db import DB, db_session, engine


class ProjectDAO(object):

    def getAllProjects(self):
        projects = db_session.query(ProjectEntity).all()

        for project in projects:
            project.release_date = str(project.release_date)
        return projects

    def getProject(self, id):
        project = db_session.query(ProjectEntity).filter(ProjectEntity.pid == id).first()
        return project

    def insertOrUpdateProject(self, project):
        db_session.add(project)
        db_session.commit()
        return project.pid