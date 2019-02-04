
from flask import request
from app import components

from app.user import userService


class UserListController(components.Controller):
    path = "/user/"
    _service = userService

    def get(self):
        return self._fetch_all()

    def post(self):
        return self._create(request.json)


class UserController(components.Controller):
    path = "/user/<int:user_id>/"
    _service = userService

    def get(self, user_id):
        return self._read(user_id)

    def put(self, user_id):
        return self._update(user_id, request.json)

    def delete(self, user_id):
        return self._delete(user_id)
