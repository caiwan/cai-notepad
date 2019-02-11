# coding=utf-8

import peewee
import random
import logging
from datetime import datetime
import jwt, bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app import components
from app.user.model import User, Permission, Role, Token, TOKEN_EXPIRATION


class UserService(components.Service):
    name = "users"
    model_class = User
    settings = {"token-expiration": TOKEN_EXPIRATION}
    secret_key = ""

    def read_item(self, item_id):
        item = self.model_class.get(User.user_id == item_id, User.is_deleted == False)
        return item

    def create_item(self, user_json):
        # This generates a random string for user_id
        user_json["user_id"] = "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ") for _ in range(32))
        user_json["password"] = bcrypt.hashpw(
            user_json["password"].encode("utf-8"),
            self.secret_key
        ).decode()
        return super().create_item(user_json)

    def update_item(self, item_id, item_json):
        # TBD
        return super().update_item(item_id, item_json)

    def delete_item(self, item_id):
        # TBD
        return super().delete_item(item_id)

    def serialize_item(self, item):
        item_json = super().serialize_item(item)
        del item_json["password"]
        return item_json

    pass


userService = UserService()


class TokenService():
    secret_key = ""
    _userService = userService

    def get(self, token_id):
        try:
            token = Token.get(Token.token_id == token_id, Token.expiration <= datetime.now())
            return token
        except Token.DoesNotExist:
            return None

    def create(self, user):
        token = Token(
            payload=self._encode(user.user_id),
            user=user
        )
        token.save()
        return token.token_id
        pass

    def renew(self, token_id):
        with components.DB.atomic():
            try:
                old_token = Token.get(Token.token_id == token_id)
                new_token = Token(
                    token_id=old_token.token_id,
                    user=old_token.user,
                    payload=self._encode(old_token.user)
                )
                new_token.save()
                old_token.delete()
                return True
            except Token.DoesNotExist:
                return False
        pass

    def revoke(self, token_id):
        try:
            Token.delete().where(Token.token_id == token_id)
        except Token.DoesNotExist:
            # Avoid hiccup
            pass
        pass

    def check(self, token_id):
        token = self.get(token_id)
        if not token:
            return False

        (user_id, client_id) = self._decode(token.payload)
        if not user_id or not client_id:
            return False

        # TODO Security Check for client id / useragent goez here
        user = self._userService.read_item(user_id)
        if user:
            return user.is_active
        return False

    def _encode(self, user_id):
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=TOKEN_EXPIRATION),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
                "cid": None  # Client id / identifier (ip, agent, etc ... )
            }
            return jwt.encode(
                payload,
                self.secret_key,
                algorithm="HS256"
            )
        except Exception as e:
            return e

    def _decode(self, auth_token):
        try:
            payload = jwt.decode(auth_token, self.secret_key)
            return (payload["sub"], payload["cid"])
        except jwt.ExpiredSignatureError:
            return (None, None)

        except jwt.InvalidTokenError:
            return (None, None)


tokenService = TokenService()


class LoginService(components.Service):
    model_class = User
    _tokenService = tokenService
    secret_key = ""

    def login(self, user_json):
        assert user_json
        invalid_msg = "Invalid username or password"
        if "username" not in user_json:
            return({"error": ["No username was given"]}, 400)
        if "password" not in user_json:
            return({"error": ["No password was given"]}, 400)

        username = user_json["username"]
        password = user_json["password"]

        try:
            user = User.get(User.name == username, User.is_deleted == False, User.is_active == True)
            if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                token = self._tokenService.create(user)
                return ({"token": token}, 200)
            else:
                return({"error": [invalid_msg]}, 400)

        except User.DoesNotExist:
            return({"error": [invalid_msg]}, 400)
        pass

    def logout(self, token):
        # ...
        pass


loginService = LoginService()
