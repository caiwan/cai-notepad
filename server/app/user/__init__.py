# coding=utf-8

from app import components
from app.user.service import UserService
from app.user.settings import SettingsService


userService = UserService()
userSettingsService = SettingsService()


class Module(components.Module):
    from app.user.model import User, Permission, Role, UserAuthenticator
    from app.user.controller import UserController, UserListController

    name = "users"
    services = [userService, userSettingsService]
    models = [User, Role, Permission, UserAuthenticator]
    controls = [UserController, UserListController]
    pass


module = Module()
