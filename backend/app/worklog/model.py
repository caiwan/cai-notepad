# coding=utf-8

import peewee
from datetime import datetime
from app import components

from app.tasks.model import Task


class Worklog(components.BaseDocumentModel):
    log_start = peewee.DateTimeField(null=False)
    log_end = peewee.DateTimeField(null=False)
    task = peewee.ForeignKeyField(Task)


class WorklogDurationCache(components.BaseModel):
    log_duration = peewee.IntegerField()
    task = peewee.ForeignKeyField(Task, backref="log_duration")
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)
