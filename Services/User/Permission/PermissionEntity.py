from Services.Database.db import Base
from sqlalchemy import Column, Integer, String


class PermissionEntity(Base):
    CAN_DO_ANYTHING = "can_do_anything"
    # permissions on project
    CAN_CREATE_PROJECT = "can_create_project"
    CAN_EDIT_PROJECT = "can_edit_project"
    # permissions on tasks
    CAN_CREATE_TASK = "can_create_task"
    CAN_EDIT_TASK = "can_edit_task"
    CAN_REMOVE_TASK = "can_remove_task"
    # permissions on user
    CAN_ADD_USER = "can_add_user"
    CAN_EDIT_USER = "can_edit_user"
    CAN_REMOVE_USER = "can_remove_user"

    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    codename = Column(String(20), nullable=True)

    def __init__(self, id, name, codename):
        self.id = id
        self.name = name
        self.codename = codename