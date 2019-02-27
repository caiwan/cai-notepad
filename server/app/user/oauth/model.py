# coding=utf-8

import peewee
from app.components import BaseModel, BaseUser


class UserAuthenticators(BaseModel):
    user = peewee.ForeignKeyField(BaseUser, backref="authenticators")
    authenticator = peewee.TextField(null=False)
    token = peewee.TextField(null=False)
