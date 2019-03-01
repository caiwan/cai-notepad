# coding=utf-8

import peewee
from app.components import BaseModel, BaseUser


class UserAuthenticators(BaseModel):
    owner = peewee.ForeignKeyField(BaseUser, backref="authenticators")
    is_deleted = peewee.BooleanField(null=False, default=False)

    authenticator = peewee.TextField(null=False)
    auth_code = peewee.TextField(null=False)
    profile = peewee.TextField(null=False)
