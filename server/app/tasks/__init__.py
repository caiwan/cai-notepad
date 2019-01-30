# coding=utf-8

from app import components
from app.tasks.model import Task


class TaskService(components.Service):
    _model_class = Task

    def __init__(self):
        super().__init__()


taskService = TaskService()


def init(app, api, models):
    from app.tasks.controller import TaskListController, TaskController
    components.register_controllers(api, [TaskController, TaskListController])
    models.extend([Task])
