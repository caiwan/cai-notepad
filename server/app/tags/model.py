# coding=utf-8

from app import components
import peewee


class Tag(components.BaseModel):
    tag = peewee.TextField(null=False)
    owner = peewee.ForeignKeyField(components.BaseUser)


class FuzzyTag(components.BaseModel):
    tag = peewee.ForeignKeyField(Tag)
    fuzzy = peewee.TextField(null=False)
