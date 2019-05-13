# coding=utf-8

import peewee
from app import components


class UserProperty(components.BaseModel):
    user = peewee.ForeignKeyField(components.BaseUser)
    module = peewee.TextField(null=False)
    key = peewee.TextField(null=False)
    value = peewee.TextField(null=False)
