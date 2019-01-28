import peewee

from app import components
from app.notes.model import Note
from app.categories.model import Category


class Task(components.BaseDocumentModel):
    title = peewee.TextField()
    is_completed = peewee.BooleanField(default=False)
    is_archived = peewee.BooleanField(default=False)
    note = peewee.ForeignKeyField(Note, null=True)
    category = peewee.ForeignKeyField(Category, null=True)
    pass
