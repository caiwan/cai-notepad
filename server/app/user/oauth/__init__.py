# coding = utf-8

import logging

from playhouse.shortcuts import model_to_dict

from app import components
from app.user.oauth.model import UserAuthenticators
from app.user.oauth.google import google_auth_code


class OauthService(components.Service):
    APP_INTEGRATIONS = "APP_INTEGRATIONS"
    model_class = UserAuthenticators
    enabled = False
    settings = {}

    def __init__(self, service_name, auth_code_handler):
        self.name = service_name
        self.auth_code_handler = auth_code_handler
        super().__init__()

    def auth_code(self, auth_code):
        if self.enabled and callable(self.auth_code_handler):
            logging.info("Yay, a 3rd party token: %s" % str(auth_code))
            self.auth_code_handler(self, auth_code)

    def _set_settings(self, app):
        if self.APP_INTEGRATIONS in app.config and self.name in app.config[self.APP_INTEGRATIONS]:
            config = app.config[self.APP_INTEGRATIONS]
            self.enabled = True
            self.settings = {
                "client_id": config[self.name]["client_id"],
                "scope": config[self.name]["scope"]
            }
        else:
            self.enabled = False


googleOauthService = OauthService("oauth-google", google_auth_code)


class DispatchOuathService(components.Service):
    name = "oauth-dispatch"
    services = {
        "google": googleOauthService
    }
    model_class = UserAuthenticators
    settings = None

    def fetch_all_items(self):
        return super().fetch_all_items()

    def create_item(self, service, item_json):
        return self._dispatch(service).create_item(item_json)

    def update_item(self, service, item_id, item_json):
        return self._dispatch(service).update_item(item_id, item_json)

    def delete_item(self, service, item_id):
        return self._dispatch(service).delete_item(item_id)

    def read_item(self, service, item_id):
        return self._dispatch(service).read_item(item_id)

    def dispatch_callback(self, service, auth_code):
        return self._dispatch(service).auth_code(auth_code)

    def _dispatch(self, service):
        if service not in self.services:
            raise components.BadRequestError("No such service %s" % service)
        return self.services[service]


    def serialize_item(self, item):
        item_json = model_to_dict(item, exclude=(
            self.model_class.owner,
            self.model_class.is_deleted,
            self.model_class.auth_code,
        ))
        return item_json


dispatchOuathService = DispatchOuathService()


class Module(components.Module):
    from app.user.oauth.controller import AuthCodeController, AuthListController
    name = "oauth"
    models = [UserAuthenticators]
    services = [
        dispatchOuathService,
        googleOauthService
    ]
    controllers = [AuthCodeController, AuthListController]

    def pre_register(self, *args, **kwargs):
        app = kwargs["app"]
        for service in self.services:
            if hasattr(service, "_set_settings"):
                service._set_settings(app)
        pass


module = Module()
