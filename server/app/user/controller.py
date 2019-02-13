# coding=utf-8

from flask import request
from app import components

from app.user import userService, loginService


class RegisterController(components.Controller):
    path = "/auth/register/"
    service = loginService

    def post(self):
        return ("Hello", 200)


class LoginController(components.Controller):
    path = "/auth/login/"
    service = loginService

    def post(self):
        return self.service.login(request.json)


class LogoutController(components.Controller):
    path = "/auth/logout/"
    service = userService

    def post(self):
        return self.service.logout()


class RefreshController(components.Controller):
    path = "/auth/renew/"
    service = loginService

    def post(self):
        return ("Hello", 200)


class PasswordResetController(components.Controller):
    path = "/auth/password_reset/"
    service = loginService

    def post(self):
        # TBD
        return({"error": ["Not implemented"]}, 501)


class UserProfileController(components.Controller):
    path = "/auth/profile/"
    service = loginService

    def get(self):
        # TBD
        return({"error": ["Not implemented"]}, 501)

    def put(self):
        # TBD
        return({"error": ["Not implemented"]}, 501)


class UserListController(components.Controller):
    path = "/users/"
    _service = userService

    def get(self):
        return self._fetch_all()

    def post(self):
        return self._create(request.json)


class UserController(components.Controller):
    path = "/users/<int:user_id>/"
    _service = userService

    def get(self, user_id):
        return self._read(user_id)

    def put(self, user_id):
        return self._update(user_id, request.json)

    def delete(self, user_id):
        return self._delete(user_id)
