from EventDAO import EventDAO


class EventService(object):
    #constants
    create_task = 'Create task'
    update_task = 'Update task'
    delete_task = 'Delete task'
    log_time = 'Log Time'
    add_project = 'Add project'
    update_project = 'Update project'
    delete_project = 'Delete project'
    add_user = 'Add user to project'
    closed_task = 'Closed task'
    start_task = 'Start task'
    reopened_task = 'Reopened task'

    def __init__(self, eventDAO=None):
        self.__DAO = eventDAO if eventDAO is not None else EventDAO()

    def getEvents(self):
        return self.__DAO.getEvents()

    def getEventByName(self, name):
        return self.__DAO.getEventByName(name)