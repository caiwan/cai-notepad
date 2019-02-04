# coding=utf-8
from app import components

from app.user.settings.model import SettingProperty


class SettingsService(components.Service):
    name = "user-settings"
    _model_class = SettingProperty

    pass


settingsService = SettingsService()


class Module(components.Module):
    name = "settings"
    services = [settingsService]
    models = [SettingProperty]
    controls = []


module = Module()
