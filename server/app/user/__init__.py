# coding=utf-8
import random
import bcrypt

from playhouse.shortcuts import dict_to_model, model_to_dict

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
        user_json = self.sanitize_fields(user_json)
        user_json["user_id"] = "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnm") for _ in range(16))
        user_json["password"] = bcrypt.hashpw(
            user_json["password"].encode("utf-8"),
            self._get_secret_key()
        ).decode()
        item = dict_to_model(self.model_class, user_json)
        item.save(force_insert=True)
        return item

    def update_item(self, item_id, item_json):
        raise RuntimeError("Not implemented")

    def delete_item(self, item_id):
        raise RuntimeError("Not implemented")

    def serialize_item(self, item):
        item_json = model_to_dict(item, exclude=(
            self.model_class.is_deleted,
            self.model_class.password
        ))
        return item_json

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
