# coding = utf-8

import logging

from flask import current_app
from app import auth, components
from app.user.oauth.model import UserAuthenticators


class OauthService(components.Service):
    APP_API_TOKENS = "APP_API_TOKENS"
    model = UserAuthenticators
    enabled = False
    settings = {}

    def __init__(self, service_name):
        self.name = service_name
        super().__init__()

    def token(self, token):
        if self.enabled:
            logging.info("Yay, a 3rd party token: %s" % str(token))

    def _set_settings(self, app):
        if self.APP_API_TOKENS in app.config and self.name in app.config[self.APP_API_TOKENS]:
            config = app.config[self.APP_API_TOKENS]
            self.enabled = True
            self.settings = {
                "client_id": config[self.name]["client_id"],
                "scope": config[self.name]["scope"]
            }
        else:
            self.enabled = False


googleOauthService = OauthService("oauth-google")


class DispatchOuathService(metaclass=components.Singleton):
    name = "oauth-dispatch"
    services = {
        "google": googleOauthService
    }
    settings = None

    def dispatch(self, service, token):
        if service not in self.services:
            raise components.BadRequestError("No such service %s" % service)
        self.services[service].token(token)
        return ("", 200)


dispatchOuathService = DispatchOuathService()


class Module(components.Module):
    from app.user.oauth.controller import OauthTokenController
    name = "oauth"
    models = [UserAuthenticators]
    services = [
        dispatchOuathService,
        googleOauthService
    ]
    controller = [OauthTokenController]

    def pre_register(self, *args, **kwargs):
        app = kwargs["app"]
        for service in self.services:
            if hasattr(service, "_set_settings"):
                service._set_settings(app)
        pass


module = Module()
