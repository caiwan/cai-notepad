# coding=utf-8

import peewee
import random
from datetime import datetime, timedelta
from app.components import BaseModel, BaseUser, BaseRole


TOKEN_EXPIRATION = 30 * 24 * 60 * 60


class Role(BaseRole):
    pass


class User(BaseUser):
    display_name = peewee.TextField(null=True)
    created = peewee.DateTimeField(null=False, default=datetime.now)
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)

    user_id = peewee.TextField(null=False, unique=True)
    is_deleted = peewee.BooleanField(null=False, default=False)
    is_active = peewee.BooleanField(null=False, default=False)

    permissions = peewee.ManyToManyField(Role, backref="users")


Permission = User.permissions.through_model


def token_expiration_time():
    return datetime.now() + timedelta(seconds=TOKEN_EXPIRATION)


def token_gen_id():
    return "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ") for _ in range(32))


class Token(BaseModel):
    token_id = peewee.CharField(unique=True, default=token_gen_id)
    user = peewee.ForeignKeyField(User)
    expiration = peewee.DateTimeField(null=False, default=token_expiration_time)
    payload = peewee.TextField(null=False)
