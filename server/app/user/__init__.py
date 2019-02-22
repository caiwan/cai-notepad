# coding=utf-8
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
        item = User.get(User.id == item_id, User.is_deleted == False)
        return item

    def create_item(self, user_json):
        user_json = self.sanitize_fields(user_json)
        user_json["password"] = bcrypt.hashpw(
            user_json["password"].encode("utf-8"),
            self._get_secret_key()
        ).decode()
        item = dict_to_model(User, user_json)
        item.save(force_insert=True)
        return item

    def update_item(self, item_id, item_json):
        raise RuntimeError("Not implemented")

    def delete_item(self, item_id):
        my_item = User.get(
            User.id == item_id,
            User.is_deleted == False
        )
        my_item.is_deleted = True
        my_item.changed()
        my_item.save()
        return my_item

    def serialize_item(self, item):
        item_json = model_to_dict(item, exclude=(
            User.is_deleted,
            User.password
        ))
        return item_json

        item_json["permissions"] = [role.name for role in item.permissions]
        return item_json

    def _get_secret_key(self):
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
