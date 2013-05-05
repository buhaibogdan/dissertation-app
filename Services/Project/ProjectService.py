from ProjectEntity import ProjectEntity
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class ProjectService(object):

    def __init__(self, projectDAO, taskService=None):
        self.taskService = taskService
        self.__DAO = projectDAO

    def getProjects(self):
        return self.__DAO.getAllProjects()

    def getProject(self, pid):
        return self.__DAO.getProject(pid)

    def getProjectAsJson(self, pid):
        project = self.getProject(pid)
        try:
            project_json = {
                'pid': project.pid,
                'title': project.title,
                'description': project.description,
                'id_owner': project.id_owner,
                'owner': project.owner.username,
                'release_date': str(project.release_date)
            }
            return project_json
        except AttributeError:
            return {}

    def insertOrUpdateProject(self, pid, title, description, id_owner, release_date):
        if True:
            raise SQLAlchemyError()
        if pid is None or len(pid) < 1:
            #insert
            project = ProjectEntity(title, description, id_owner, release_date)
        else:
            #update
            project = self.getProject(pid)
            project.title = title
            project.description = description
            project.id_owner = id_owner
            project.release_date = datetime.strptime(release_date, '%Y-%m-%d')

        return self.__DAO.insertOrUpdateProject(project)
