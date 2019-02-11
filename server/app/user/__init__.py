# coding=utf-8

from flask import g
from flask.ext.principal import identity_loaded, RoleNeed, UserNeed

from app import components

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
        (
            app,
            auth,
            principal
        ) = (
            kwargs["app"],
            kwargs["auth"],
            kwargs["principal"],
        )

        @auth.verify_token
        def verify_token(token_id):
            user = tokenService.verify(token_id)
            if not user:
                g.current_user = None
                return False
            g.current_user = user
            return True

        @principal.identity_loader
        def load_identity(sender, identity):
            identity.user = g.current_user
            if hasattr(g.current_user, 'id'):
                identity.provides.add(UserNeed(g.current_user.id))
            if hasattr(g.current_user, 'roles'):
                for role in g.current_user.roles:
                    identity.provides.add(RoleNeed(role.name))

        secret_key = app.config["SECRET_KEY"]
        loginService.secret_key = secret_key
        userService.secret_key = secret_key
        tokenService.secret_key = secret_key


module = Module()
