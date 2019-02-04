# coding=utf-8

import peewee
from app import components

from app.notes.model import Note
from app.tasks.model import Task


class BaseSync(components.BaseDocumentModel):
    foreign_id = peewee.TextField()
    provider = peewee.TextField()


class NoteSync(BaseSync):
    note = peewee.ForeignKeyField(Note)


class TaskSync(BaseSync):
    task = peewee.ForeignKeyField(Task)
