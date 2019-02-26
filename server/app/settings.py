# coding=utf-8

# coding=utf-8
from app import components

from app.user.settings.model import UserProperty


class SettingsService(components.Service):
    name = "app-settings"
    model_class = UserProperty

    # FK

    pass


settingsService = SettingsService()


class SettingsController(components.Controller):
    service = settingsService()
    path = "/settings"

    def get(self):
        return self.service.get_settings()


class Module(components.Module):
    name = "app-settings"
    services = [settingsService]
    models = []
    controllers = []
    pass


module = Module()
