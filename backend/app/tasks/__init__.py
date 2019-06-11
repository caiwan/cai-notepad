# coding=utf-8
from datetime import datetime

from app import components
from app.tasks.model import Task

from app.categories import categoryService


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

    def fetch_all_items(self, category_filter, milestone_filter):
        user_id = components.current_user_id()
        category_select = categoryService.category_filter_helper(Task, user_id, category_filter)
        milestone_select = []
        # milestone_filter == "all"
        # milestone_filter == "unassigned"
        # else ...

        return Task.select(Task).where(
            Task.is_deleted == False,
            *category_select,
            *milestone_select,
            Task.owner_id == user_id
        ).order_by(Task.order.asc())
        pass

    def sanitize_fields(self, item_json):
        if "due_date" in item_json:
            due_date = datetime.fromtimestamp(int(item_json["due_date"])).date() if item_json["due_date"] else None
            item_json["due_date"] = due_date
        return super().sanitize_fields(item_json)


taskService = TaskService()


class Module(components.Module):
    from app.tasks.controller import TaskListController, TaskController
    name = "tasks"
    services = [taskService]
    models = [Task]
    controllers = [TaskController, TaskListController]


module = Module()
