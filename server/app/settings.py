# coding=utf-8

# coding=utf-8
from app import components

from app.user.settings.model import UserProperty


class SettingsService(components.Service):
    name = "app-settings"
    model_class = UserProperty

    def __init__(self, *args, **kwargs):
        self.settings = {}
        super().__init__(*args, **kwargs)

    def set_settings(self, settings):
        self.settings = settings

    def get_settings(self):
        return self.settings, 200

    pass


settingsService = SettingsService()


class SettingsController(components.Controller):
    service = settingsService
    path = "/settings"

    def get(self):
        return self.service.get_settings()


class Module(components.Module):
    name = "app-settings"
    services = [settingsService]
    models = []
    controllers = [SettingsController]
    pass


module = Module()
