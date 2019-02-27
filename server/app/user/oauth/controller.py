# coding=utf-8
from flask_restful import request
from app import components
from app.user.oauth import dispatchOuathService


class OauthTokenController(components.Controller):
    path = "/auth/oauth/<service_name>/client_id/"
    service = dispatchOuathService

    def get(self, service_name):
        token = request.args.get("token")
        if not token:
            raise components.BadRequestError()
        self.dispatch_request(service_name, token)

    def post(self, service_name):
        if "token" not in request.json:
            raise components.BadRequestError()
        self.dispatch_request(service_name, request.json["token"])
