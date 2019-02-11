# coding=utf-8
from app import components

from flask_security import PeeweeUserDatastore

from app.user.service import userService, loginService, tokenService
from app.user.model import User, Role, Permission, Token
from app.user.controller import LoginController, LogoutController, RegisterController, RefreshController, PasswordResetController
from app.user.controller import UserController, UserListController


class Module(components.Module):

    name = "users"
    services = [userService, loginService]
    models = [User, Role, Permission, Token]
    controllers = [
        LoginController,
        LogoutController,
        RegisterController,
        RefreshController,
        PasswordResetController,
        UserController,
        UserListController
    ]

    def pre_register(self, *args, **kwargs):
        assert "app" in kwargs
        # assert "security" in kwargs

        (
            app,
            auth
        ) = (
            kwargs["app"],
            kwargs["auth"]
        )

        @auth.verify_token
        def verify_token(token_id):
            return tokenService.verify(token_id)

        secret_key = app.config["SECRET_KEY"]
        loginService.secret_key = secret_key
        userService.secret_key = secret_key
        tokenService.secret_key = secret_key


module = Module()
