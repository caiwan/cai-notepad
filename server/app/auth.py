# coding=utf-8

# import logging
from datetime import datetime, timedelta
import jwt, bcrypt
import random

import peewee

from flask import g, current_app
from flask_httpauth import HTTPTokenAuth
import flask_principal as p
from flask_principal import Principal

from app import components

TOKEN_EXPIRATION = 30 * 24 * 60 * 60


auth_api = HTTPTokenAuth(scheme="Bearer")
principal = Principal(use_sessions=False, skip_static=True)


class Role(components.BaseRole):
    pass


class User(components.BaseUser):
    display_name = peewee.TextField(null=True)
    created = peewee.DateTimeField(null=False, default=datetime.now)
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)

    user_id = peewee.TextField(null=False, unique=True)
    is_deleted = peewee.BooleanField(null=False, default=False)
    is_active = peewee.BooleanField(null=False, default=False)

    permissions = peewee.ManyToManyField(Role, backref="users")

    def changed(self):
        self.edited = datetime.now()


Permission = User.permissions.through_model


def token_expiration_time():
    return datetime.now() + timedelta(seconds=TOKEN_EXPIRATION)


def token_gen_id():
    return "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ") for _ in range(32))


class Token(components.BaseModel):
    token_id = peewee.CharField(unique=True, default=token_gen_id)
    user = peewee.ForeignKeyField(User)
    expiration = peewee.DateTimeField(null=False, default=token_expiration_time)
    payload = peewee.TextField(null=False)


class TokenService():
    def get(self, token_id):
        try:
            token = Token.get(Token.token_id == token_id, Token.expiration >= datetime.now())
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
            # logging.info("Lol?" + token_id)
            token = Token.get(Token.token_id == token_id)
            token.delete_instance()
            # Token.delete().where(Token.token_id == token_id)
        except Token.DoesNotExist:
            # Avoid hiccup
            pass
        pass

    def verify(self, token_id):
        token = self.get(token_id)
        if not token:
            # logging.info("no token")
            return None

        (user_id, client_id) = self._decode(token.payload)
        if not user_id or not client_id:
            # logging.info("no uid or cid %s %s" % (user_id, client_id))
            return None

        # TODO Security Check for client id / useragent goez here

        user = User.get(User.user_id == user_id, User.is_deleted == False, User.is_active == True)
        if user:
            return user if user.is_active else None
        return None

    def _encode(self, user_id):
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=0, seconds=TOKEN_EXPIRATION),
                "iat": datetime.utcnow(),
                "sub": user_id,
                "cid": "Some client id will go here at some point"  # Client id / identifier (ip, agent, etc ... )
            }
            return jwt.encode(
                payload,
                self.get_secret_key(),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    def _decode(self, auth_token):
        try:
            payload = jwt.decode(auth_token, self.get_secret_key())
            return (payload["sub"], payload["cid"])
        except jwt.ExpiredSignatureError:
            # logging.info("no signature %s" % auth_token)
            return (None, None)

        except jwt.InvalidTokenError:
            # logging.info("iv token %s" % auth_token)
            return (None, None)

    def get_secret_key(self):
        return current_app.config["SECRET_KEY"]


tokenService = TokenService()


class LoginService(components.Service):
    model_class = User
    _tokenService = tokenService

    def login(self, user_json):
        assert user_json
        if "username" not in user_json or "password" not in user_json:
            return components.error_handler("Bad request", "No username or password was given")

        username = user_json["username"]
        password = user_json["password"]

        invalid_msg = "Invalid username or password"
        try:
            user = User.get(User.name == username, User.is_deleted == False, User.is_active == True)
            if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                token = self._tokenService.create(user)
                return ({"token": token}, 200)
            else:
                return components.error_handler("Authentication", invalid_msg, 200)

        except User.DoesNotExist:
            return components.error_handler("Authentication", invalid_msg, 200)
        pass

    def logout(self):
        auth_data = auth_api.get_auth()
        if auth_data:
            self._tokenService.revoke(auth_data["token"])
        return ("", 200)

    def renew(self, token_id):
        self.__tokenService.renew(token_id)
        return ("", 200)

    def get_profile(self):
        if not hasattr(g, "current_user") or not g.current_user:
            return (None, 200)
        # user = g.current_user
        # TODO ...
        pass

    def set_profile(self, payload):
        if not hasattr(g, "current_user") or not g.current_user:
            return (None, 200)
        # user = g.current_user
        # TODO ...
        pass


loginService = LoginService()


@auth_api.verify_token
def verify_token(token_id):
    # logging.info("Token %s", str(token_id))
    user = tokenService.verify(token_id)
    if not user:
        g.current_user = None
        return False
    g.current_user = user
    # logging.info("User %s %s", user.id, user.user_id)
    return True


@principal.identity_loader
def load_identity():
    if not hasattr(g, "current_user") or not g.current_user:
        return p.AnonymousIdentity()
    # logging.info("Current user %s %d " % (g.current_user.name, g.current_user.id))
    identity = p.Identity(g.current_user.user_id)
    identity.user = g.current_user
    if hasattr(g.current_user, "id"):
        identity.provides.add(p.UserNeed(g.current_user.id))
    else:
        return p.AnonymousIdentity()
        # logging.info("Has no id")
    if hasattr(g.current_user, "permissions"):
        for role in g.current_user.permissions:
            identity.provides.add(p.RoleNeed(role.name.upper()))
        # logging.info("Current user permissions: %s" % (", ".join([role.name for role in g.current_user.permissions])))
    else:
        # logging.info("Has no permissions")
        pass
    return identity


admin_permission = p.Permission(p.RoleNeed("ADMIN"))


def error_handler(f):
    auth_api.error_handler(f)


def login_required(f):
    return auth_api.login_required(f)


def current_user():
    if not hasattr(g, "current_user") or not g.current_user:
        return None
    else:
        return g.current_user
