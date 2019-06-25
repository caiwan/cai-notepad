# coding = utf-8

import logging
import json

from playhouse.shortcuts import model_to_dict

from app import components
from app.user.oauth.model import UserAuthenticator
from app.user.oauth.google import google_auth_code


class OauthService(metaclass=components.Singleton):
    APP_INTEGRATIONS = "APP_INTEGRATIONS"

    def __init__(self, service_name, auth_code_handler):
        self.name = service_name
        self.auth_code_handler = auth_code_handler
        self.enabled = False
        self.settings = {}
        super().__init__()

    def token_callback(self, tokens):
        if self.enabled and callable(self.auth_code_handler):
            return self.auth_code_handler(self, tokens)

    def _set_settings(self, app):
        if self.APP_INTEGRATIONS in app.config and self.name in app.config[self.APP_INTEGRATIONS]:
            config = app.config[self.APP_INTEGRATIONS][self.name]
            self.enabled = "enabled" in config and bool(config["enabled"])
            self.settings = {
                "enabled": config["enabled"],
                "client_id": config["client_id"],
                "scope": config["scope"]
            }
        else:
            self.enabled = False
            self.settings = {}


googleOauthService = OauthService("oauth-google", google_auth_code)


class DispatchOuathService(components.Service):
    name = "oauth-dispatch"
    services = {
        "google": googleOauthService
    }
    model_class = UserAuthenticator
    settings = None

    def delete_item(self, token_id):
        user_id = components.current_user_id()
        item = UserAuthenticator.select(
            UserAuthenticator
        ).join(
            components.BaseUser, on=(UserAuthenticator.owner == components.BaseUser.id)
        ).where(
            UserAuthenticator.id == token_id,
            UserAuthenticator.owner.id == user_id
        ).get()
        item.delete_item()

    def dispatch_callback(self, service, token_obj):
        return self._dispatch(service).token_callback(token_obj)

    def _dispatch(self, service):
        if service not in self.services:
            raise components.BadRequestError("No such service %s" % service)
        return self.services[service]

    def serialize_item(self, item):
        item_json = model_to_dict(item, only=(UserAuthenticator.id, UserAuthenticator.idp_id,))
        item_json["profile"] = json.loads(item.profile)
        return item_json


dispatchOuathService = DispatchOuathService()


class Module(components.Module):
    from app.user.oauth.controller import AuthCodeController, AuthListController, AuthController
    name = "oauth"
    models = [UserAuthenticator]
    services = [
        dispatchOuathService,
        googleOauthService
    ]
    controllers = [AuthCodeController, AuthListController, AuthController]

    def pre_register(self, *args, **kwargs):
        app = kwargs["app"]
        for service in self.services:
            if hasattr(service, "_set_settings"):
                service._set_settings(app)
        pass


module = Module()
