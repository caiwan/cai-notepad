# coding=utf-8
import peewee
from app import components

from app.tags.model import Tag
from app.categories.model import Category


class Milestone(components.BaseDocumentModel):
    name = peewee.TextField()
    description = peewee.TextField()
    due_date = peewee.DateTimeField(null=True, default=None, formats=["%s", "%Y-%m-%d"])
    tags = peewee.ManyToManyField(Tag)
    category = peewee.ForeignKeyField(Category, null=True, default=None)
    pass


TaggedMilestone = Milestone.tags.through_model
