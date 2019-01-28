# coding=utf-8

import peewee
from app import components

from app.tags.model import Tag
from app.categories.model import Category
# from milestones.model import Milestone


class Note(components.BaseDocumentModel):
    title = peewee.TextField()
    content = peewee.TextField()
    is_archived = peewee.BooleanField(default=False)
    is_pinned = peewee.BooleanField(default=False)
    tags = peewee.ManyToManyField(Tag)
    category = peewee.ForeignKeyField(Category, null=True, default=None)
    due_date = peewee.DateTimeField(null=True, default=None)
    # -> Tasks will have milestones, not the notes that were taken
    # milestone = peewee.ForeignKeyField(Milestone, null=True, default=None)
    # decoration = ? (like colors, etc)


TaggedNote = Note.tags.get_through_model()
