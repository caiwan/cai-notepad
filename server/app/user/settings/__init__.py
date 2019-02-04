# coding=utf-8
from app import components

from app.user.settings.model import UserProperty


class UserSettingsService(components.Service):
    name = "user-settings"
    model_class = UserProperty

    pass
