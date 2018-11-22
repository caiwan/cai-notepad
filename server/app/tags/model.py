# coding=utf-8

import components
import peewee

class Tag(components.BaseModel):
    tag = peewee.TextField(null=False, unique=True)

class FuzzyTag(components.BaseModel):
    tag = peewee.ForeignKeyField(Tag)
    fuzzy = peewee.TextField(null=False)
