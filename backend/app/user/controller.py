# coding=utf-8

from flask import request

from app import components
from app import auth

from app.user import userService


class RegisterController(components.Controller):
    path = "/auth/register/"
    service = auth.loginService

    def post(self):
        return ("OwO", 403)


class LoginController(components.Controller):
    path = "/auth/login/"
    service = auth.loginService

    def post(self):
        return self.service.login(request.json)


class LogoutController(components.Controller):
    path = "/auth/logout/"
    service = auth.loginService

    @auth.login_required
    def get(self):
        return self.service.logout()

    @auth.login_required
    def post(self):
        return self.service.logout()


class RefreshController(components.Controller):
    path = "/auth/renew/"
    service = auth.loginService

    @auth.login_required
    def post(self):
        return ("Hello", 200)


class PasswordResetController(components.Controller):
    path = "/auth/password_reset/"
    service = auth.loginService

    @auth.login_required
    def post(self):
        # TBD
        # return({"error": ["Not implemented"]}, 501)
        raise components.MethodNotImplemented()


# User admin


class UserProfileController(components.Controller):
    path = "/auth/profile/"
    service = auth.loginService

    @auth.login_required
    def get(self):
        return self.service.get_profile()

    @auth.login_required
    def put(self):
        raise components.MethodNotImplemented()


class UserListController(components.Controller):
    path = "/users/"
    _service = userService

    @auth.admin_permission.require()
    def get(self):
        return self._fetch_all()

    @auth.admin_permission.require()
    def post(self):
        import logging
        from flask import g
        logging.info("Identity %s" % g.identity)
        return self._create(request.json)


class UserController(components.Controller):
    path = "/users/<int:user_id>/"
    _service = userService

    @auth.admin_permission.require()
    def get(self, user_id):
        return self._read(user_id)

    @auth.admin_permission.require()
    def put(self, user_id):
        return self._update(user_id, request.json)

    @auth.admin_permission.require()
    def delete(self, user_id):
        return self._delete(user_id)
