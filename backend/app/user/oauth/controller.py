# coding=utf-8
from flask_restful import request
from app import auth, components
from app.user.oauth import dispatchOuathService


class AuthCodeController(components.Controller):
    path = "/auth/oauth/cb/<string:service_name>/"
    _service = dispatchOuathService

    @auth.login_required
    def post(self, service_name):
        self._service.dispatch_callback(service_name, request.json)
        return "", 201


class AuthListController(components.Controller):
    path = "/auth/oauth/authenticators/"
    _service = dispatchOuathService

    @auth.login_required
    def get(self):
        return self._fetch_all()


class AuthController(components.Controller):
    path = "/auth/oauth/authenticators/<int:token_id>"
    _service = dispatchOuathService

    @auth.login_required
    def delete(self, token_id):
        return self._delete(token_id)
