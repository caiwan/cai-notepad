# coding=utf-8

from app import components
from app.user.service import UserService


userService = UserService()


class Module(components.Module):
    from app.user.model import User, Permission, Role, UserAuthenticator
    from app.user.controller import UserController, UserListController

    name = "users"
    services = [userService]
    models = [User, Role, Permission, UserAuthenticator]
    controls = [UserController, UserListController]
    pass


module = Module()
