from ProjectEntity import ProjectEntity
from Services.Database.db import DB, db_session, engine
import json

class ProjectService(object):

    def __init__(self, taskService):
        self.taskService = taskService

    def getProjects(self):
        projects = db_session.query(ProjectEntity).all()
        p = []
        for project in projects:
            p.append({'pid':project.pid,
                      'title':project.title,
                        'description':project.description,
                        'owner':project.id_owner,
                        'release_date':str(project.release_date)})

        return json.dumps(p)

    def getProject(self, id):
        pass

    def saveProject(self, newProject):
        pass