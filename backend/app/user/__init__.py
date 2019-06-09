# coding=utf-8

import logging

from playhouse.shortcuts import dict_to_model, model_to_dict

from app import components
from app import auth

from app.user.model import User
from app.auth import TOKEN_EXPIRATION


class UserService(components.Service):
    name = "users"
    model_class = User
    settings = {"token-expiration": TOKEN_EXPIRATION}

    def read_item(self, item_id):
        item = User.get(User.id == item_id, User.is_deleted == False)
        return item

    def fetch_all_items(self):
        return User.select(
            User
        ).where(
            User.is_deleted == False,
        ).objects()

    def create_item(self, user_json):
        user_json = self.sanitize_fields(user_json)
        if "name" not in user_json or "password" not in user_json:
            raise components.BadRequestError("Username or password missing")
        user_json["password"] = auth.hash_password(user_json["password"])
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

        item_json["permissions"] = [role.name for role in item.permissions]

        logging.debug("--- SERIALIZE USER TOKEN: %s" %(str(item_json)))

        return item_json


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
