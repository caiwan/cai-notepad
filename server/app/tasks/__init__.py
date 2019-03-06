# coding=utf-8

from app import components
from app.tasks.model import Task


class TaskService(components.Service):
    name = "tasks"
    model_class = Task

    settings = {
        "priority_colors": [
            {"name": "red", "value": 6},
            {"name": "orange", "value": 5},
            {"name": "yellow", "value": 4},
            {"name": "green", "value": 3},
            {"name": "blue", "value": 2},
            {"name": "purple", "value": 1},
            {"name": "none", "value": 0},
        ]
    }

    def __init__(self):
        super().__init__()


taskService = TaskService()


class Module(components.Module):
    from app.tasks.controller import TaskListController, TaskController
    name = "tasks"
    services = [taskService]
    models = [Task]
    controllers = [TaskController, TaskListController]


module = Module()
