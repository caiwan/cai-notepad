# coding=utf-8

import peewee
from app.components import BaseModel, BaseUser


class UserAuthenticator(BaseModel):
    owner = peewee.ForeignKeyField(BaseUser, backref="authenticators")

    idp_id = peewee.TextField(null=False)
    access_token = peewee.TextField(null=False)
    id_token = peewee.TextField(null=False)
    token_type = peewee.TextField(null=False, default="Bearer")

    expires_at = peewee.DateTimeField(null=False)

    profile = peewee.TextField(null=False)
