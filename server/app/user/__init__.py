# coding=utf-8
import random
import bcrypt

from app import components

from app.user.model import User
from app.auth import TOKEN_EXPIRATION
from flask import current_app


class UserService(components.Service):
    name = "users"
    model_class = User
    settings = {"token-expiration": TOKEN_EXPIRATION}

    def read_item(self, item_id):
        item = self.model_class.get(User.user_id == item_id, User.is_deleted == False)
        return item

    def create_item(self, user_json):
        raise RuntimeError("Not implemented")
        # user_json["user_id"] = "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(16))
        # user_json["password"] = bcrypt.hashpw(
        # user_json["password"].encode("utf-8"),
        # self._get_secret_key()
        # ).decode()
        # return super().create_item(user_json)

    def update_item(self, item_id, item_json):
        raise RuntimeError("Not implemented")
        # return super().update_item(item_id, item_json)

    def delete_item(self, item_id):
        raise RuntimeError("Not implemented")
        # return super().delete_item(item_id)

    def serialize_item(self, item):
        item_json = super().serialize_item(item)
        # del item_json["password"]
        item_json["permissions"] = [role.name for role in item.permissions]
        return item_json

    def _get_secret_key():
        return current_app.config["SECRET_KEY"]


userService = UserService()


class Module(components.Module):
    from app.user import model, controller
    name = "users"
    services = [userService]
    models = [model.User, model.Role, model.Permission, model.Token]
    controllers = [
        controller.LoginController,
        controller.LogoutController,
        controller.RegisterController,
        controller.RefreshController,
        controller.PasswordResetController,
        controller.UserProfileController,
        controller.UserController,
        controller.UserListController
    ]


module = Module()
