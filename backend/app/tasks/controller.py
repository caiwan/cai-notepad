
from flask import request
from app import components, auth

from app.tasks import taskService


class TaskListController(components.Controller):
    path = "/tasks/"
    _service = taskService

    @auth.login_required
    def get(self):
        category_filter = request.args.get("category", default="all", type=str)
        milestone_filter = request.args.get("milestone", default="all", type=str)
        return self._fetch_all(category_filter, milestone_filter)

    @auth.login_required
    def post(self):
        return self._create(request.json)


class TaskController(components.Controller):
    path = "/tasks/<int:task_id>/"
    _service = taskService

    @auth.login_required
    def get(self, task_id):
        return self._read(task_id)

    @auth.login_required
    def put(self, task_id):
        return self._update(task_id, request.json)

    @auth.login_required
    def delete(self, task_id):
        return self._delete(task_id)
