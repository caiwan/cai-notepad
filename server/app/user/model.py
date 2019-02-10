# coding=utf-8

import peewee
from datetime import datetime, timedelta
from app.components import BaseModel, BaseUser, BaseRole


TOKEN_EXPIRATION = 30 * 24 * 60 * 60


class Role(BaseRole):
    pass


class User(BaseUser):
    display_name = peewee.TextField()
    created = peewee.DateTimeField(null=False, default=datetime.now)
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)

    user_id = peewee.TextField(null=False, unique=True)
    is_deleted = peewee.BooleanField(null=False, default=False)
    is_active = peewee.BooleanField(null=False, default=False)

    permissions = peewee.ManyToManyField(Role, backref="users")


Permission = User.permissions.through_model


def token_expiration_time():
    return datetime.datetime.now() + timedelta(seconds=TOKEN_EXPIRATION)


class Token(BaseModel):
    token_id = peewee.CharField(unique=True)
    user = peewee.ForeignKeyField(User)
    expiration = peewee.DateTimeField(null=True, default=token_expiration_time)
    payload = peewee.TextField(null=False)
