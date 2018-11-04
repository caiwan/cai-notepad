# coding=utf-8

from flask import request
import components

import mongoengine


## -- model

class Task(components.BaseModel):
    title = mongoengine.StringField(max_length=512)
    completed = mongoengine.BooleanField(default=False)
    pass


# --- controllers

class TaskListController(components.Controller):
    path = "/tasks/"

    def get(self):
        return self._fetch_all(Task)

    def post(self):
        return self._create(Task, request)


class TaskController(components.Controller):
    path = "/tasks/<string:task_id>/"

    def get(self, task_id):
        return self._read(Task, task_id)

    def put(self, task_id):
        return self._update(Task, request, task_id)

    def delete(self, task_id):
        return self._delete(Task, task_id)


def init(app, api, models):
    components.register_controllers(api, [TaskController, TaskListController])
    models += [Task]
