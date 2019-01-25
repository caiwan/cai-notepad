# coding=utf-8

import components
from tasks.model import Task


class TaskService(components.Service):
    _model_class = Task
    pass

taskService = TaskService()

def init(app, api, models):
    from tasks.controller import TaskListController, TaskController
    components.register_controllers(api, [TaskController, TaskListController])
    models.extend([Task])
