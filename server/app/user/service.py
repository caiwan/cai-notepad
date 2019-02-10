# coding=utf-8

import peewee
import random
from datetime import datetime
import jwt, bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app import components
from app.user.model import User, Permission, Role, Token, TOKEN_EXPIRATION


class TokenService(components.Service):
    model_class = Token
    secret_key = ""

    def read_item(self, token_id):
        assert self.model_class
        token = self.model_class.get(self.model_class.token == token_id, self.model_class.expiration >= datetime.now())
        if not token:
            raise peewee.DoesNotExist()
        return token

    def add_token(self, user):
        # Generate JWT token or sometihng
        # https://realpython.com/token-based-authentication-with-flask/#jwt-setup
        return "token"
        pass

    def revoke_token(self, token_id):
        pass

    def check_token(self, token_id):
        pass

    def _gen_token_id():
        return "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ") for _ in range(32))

    def _encode_auth_token(self, user_id):
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=TOKEN_EXPIRATION),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id
            }
            return jwt.encode(
                payload,
                self.secret_key,
                algorithm="HS256"
            )
        except Exception as e:
            return e

    def _decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, self.secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None

        except jwt.InvalidTokenError:
            return None


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
            if user and bcrypt.check_password_hash(user.password, password):
                token = self._tokenService.add_token(user)
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
        user_json["user_id"] = "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ") for _ in range(32)),
        user_json["password"] = bcrypt.generate_password_hash(user_json["password"], 256).decode()
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
