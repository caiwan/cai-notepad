import peewee

from app import components
from app.notes.model import Note
from app.categories.model import Category


class Task(components.BaseDocumentModel):
    title = peewee.TextField()
    is_completed = peewee.BooleanField(default=False)
    is_archived = peewee.BooleanField(default=False)
    note = peewee.ForeignKeyField(Note, null=True, backref="tasks")
    category = peewee.ForeignKeyField(Category, null=True, backref="tasks")
    due_date = peewee.DateTimeField(null=True, default=None, formats=["%s"])
    color = peewee.IntegerField(null=False, default=0)
    order = peewee.IntegerField(null=False, default=0)
