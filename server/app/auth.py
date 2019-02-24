# coding=utf-8

import logging
from datetime import datetime, timedelta
import jwt
import bcrypt
from uuid import UUID, uuid4

import peewee
from playhouse.shortcuts import model_to_dict

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

    user_ref_id = peewee.UUIDField(null=False, unique=True, default=uuid4)
    is_deleted = peewee.BooleanField(null=False, default=False)
    is_active = peewee.BooleanField(null=False, default=False)

    permissions = peewee.ManyToManyField(Role, backref="users")

    def changed(self):
        self.edited = datetime.now()


Permission = User.permissions.through_model


def token_expiration_time():
    return datetime.now() + timedelta(seconds=TOKEN_EXPIRATION)


# def token_gen_id():
    # return "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ") for _ in range(32))


class Token(components.BaseModel):
    id = peewee.UUIDField(primary_key=True, default=uuid4)
    user = peewee.ForeignKeyField(User)
    expiration = peewee.DateTimeField(
        null=False, default=token_expiration_time)
    payload = peewee.TextField(null=False)


class TokenService():
    def get(self, id):
        try:
            if not id:
                return None
            token = Token.get(
                Token.id == UUID(id), Token.expiration >= datetime.now())
            return token
        except Token.DoesNotExist:
            return None

    def create(self, user):
        token = Token(
            payload=self._encode(user.user_ref_id),
            user=user
        )
        token.save(force_insert=True)
        return token.id
        pass

    def renew(self, id):
        with components.DB.atomic():
            try:
                token = Token.get(Token.id == UUID(id))
                token.payload = self._encode(token.user.user_ref_id)
                token.save()
                return True
            except Token.DoesNotExist:
                return False
        pass

    def revoke(self, id):
        try:
            token = Token.get(Token.id == UUID(id))
            token.delete_instance()
        except Token.DoesNotExist:
            # Avoid exception when try delete the same twice
            # This should not happen anyways.
            pass
        pass

    def verify(self, token_id):
        token = self.get(token_id)
        if not token:
            logging.debug("no valid token")
            return None

        (user_ref_id, client_info) = self._decode(token.payload)
        if not user_ref_id or not client_info:
            logging.debug("Token has no ref_id or client %s %s" %
                          (user_ref_id, client_info))
            return None

        # TODO Security Check for client id / useragent goez here

        user = User.get(User.user_ref_id == user_ref_id,
                        User.is_deleted == False, User.is_active == True)
        if user:
            return user if user.is_active else None
        return None

    def _encode(self, user_ref_id):
        try:
            # Store some client info (ip, agent, etc ... ) to avoid token/session theft
            client_info = "Some client id will go here at some point"
            payload = {
                "exp": datetime.utcnow() + timedelta(days=0, seconds=TOKEN_EXPIRATION),
                "iat": datetime.utcnow(),
                "sub": str(user_ref_id),
                "client_info": client_info
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
            return (payload["sub"], payload["client_info"])
        except jwt.ExpiredSignatureError:
            logging.debug("no signature %s" % auth_token)
            return (None, None)

        except jwt.InvalidTokenError:
            logging.debug("iv token %s" % auth_token)
            return (None, None)

    def get_secret_key(self):
        return current_app.config["SECRET_KEY"]


tokenService = TokenService()


class LoginService(components.Service):
    model_class = User
    _tokenService = tokenService

    invalid_usr_msg = "Invalid credentials were given or user does not exist"

    def login(self, user_json):
        assert user_json
        if "username" not in user_json or "password" not in user_json:
            raise components.AuthorizationError(
                payload={"reason": self.invalid_usr_msg})

        username = user_json["username"]
        password = user_json["password"]

        try:
            user = User.get(User.name == username,
                            User.is_deleted == False, User.is_active == True)
            if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                token = self._tokenService.create(user)
                return ({"token": token}, 200)
            else:
                raise components.AuthorizationError()

        except User.DoesNotExist:
            raise components.AuthorizationError(
                payload={"reason": self.invalid_usr_msg})
        pass

    def logout(self):
        auth_data = auth_api.get_auth()
        if auth_data:
            self._tokenService.revoke(auth_data["token"])
        return ("", 200)

    def renew(self, id):
        self.__tokenService.renew(id)
        return ("", 200)

    def get_profile(self):
        # if not hasattr(g, "current_user") or not g.current_user:
        # return (None, 200)
        # user = g.current_user
        # TODO ...
        pass

    def set_profile(self, payload):
        # if not hasattr(g, "current_user") or not g.current_user:
        # return (None, 200)
        # user = g.current_user
        # TODO ...
        pass


loginService = LoginService()


@auth_api.verify_token
def verify_token(id):
    # logging.info("Token %s", str(id))
    user = tokenService.verify(id)
    if not user:
        g.current_user = None
        return False
    g.current_user = user
    logging.debug("User authenticated id=%s ref_id=%s",
                  user.id, user.user_ref_id)
    return True


@principal.identity_loader
@auth_api.login_required
def load_identity():
    if not hasattr(g, "current_user") or not g.current_user:
        logging.debug("User identity as Anonymous")
        return p.AnonymousIdentity()
    identity = p.Identity(g.current_user.id)
    identity.user = g.current_user
    logging.debug("Current user %s %d " % (g.current_user.name, g.current_user.id))
    identity.provides.add(p.UserNeed(g.current_user.id))
    if g.current_user.permissions.count():
        for role in g.current_user.permissions:
            identity.provides.add(p.RoleNeed(role.name.upper()))
        logging.debug("User has permissions: %s" % (
            ", ".join([role.name for role in g.current_user.permissions])))
    else:
        logging.debug("User Has no permissions")
        pass
    return identity


@principal.identity_saver
def save_identity(identity):
    g.identity = identity


admin_permission = p.Permission(p.RoleNeed("ADMIN"))


def error_handler(f):
    auth_api.error_handler(f)


def login_required(f):
    return auth_api.login_required(f)


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        current_app.config["SECRET_KEY"]
    )


# For maintanance only
def _adduser(username, password):
    user = User(
        name=username,
        password=hash_password(password)
    )
    user.save(force_insert=True)
    return user.id


def _rmuser(user_id):
    user = User.get(User.id == int(user_id))
    user.delete_instance()


def _listusers():
    return [model_to_dict(user) for user in User.select()]


def _addrole(role):
    role = Role(name=role)
    role.save()


def _rmrole(role):
    role = Role.get(Role.name == role)
    role.delete_instance()


def _listroles():
    return [model_to_dict(role) for role in Role.select()]
