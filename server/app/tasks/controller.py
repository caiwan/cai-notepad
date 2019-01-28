
from flask import request
from app import components

from app.tasks import taskService


class TaskListController(components.Controller):
    path = "/tasks/"
    _service = taskService

    def get(self):
        return self._fetch_all()

    def post(self):
        return self._create(request.json)


class TaskController(components.Controller):
    path = "/tasks/<int:task_id>/"
    _service = taskService

    def get(self, task_id):
        return self._read(task_id)

    def put(self, task_id):
        return self._update(task_id, request.json)

    def delete(self, task_id):
        return self._delete(task_id)
