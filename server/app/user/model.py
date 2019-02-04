# coding=utf-8

import peewee
from datetime import datetime
from app.components import BaseModel, BaseUser, BaseRole


class Role(BaseRole):
    created = peewee.DateTimeField(null=False, default=datetime.now)
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)

    is_deleted = peewee.BooleanField(null=False, default=False)
    is_active = peewee.BooleanField(null=False, default=False)
    pass


class User(BaseUser):
    handle = peewee.TextField()
    display_name = peewee.TextField()
    password = peewee.TextField()
    permissions = peewee.ManyToManyField(Role)

    created = peewee.DateTimeField(null=False, default=datetime.now)
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)

    is_deleted = peewee.BooleanField(null=False, default=False)
    is_active = peewee.BooleanField(null=False, default=False)


class UserAuthenticator(BaseModel):
    user = peewee.ForeignKeyField(User)
    authenticator = peewee.TextField()
    token = peewee.TextField()

    is_deleted = peewee.BooleanField(null=False, default=False)
    is_active = peewee.BooleanField(null=False, default=False)
    pass


# +OAuth tokens?


Permission = User.permissions.get_through_model()
