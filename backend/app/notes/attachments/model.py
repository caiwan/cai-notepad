# coding=utf-8

import peewee
from app import components

from app.notes.model import Note


class NoteAttachment(components.BaseModel):
    name = peewee.TextField()
    attachment_id = peewee.TextField()
    provider = peewee.TextField()
    note = peewee.ForeignKeyField(Note)
