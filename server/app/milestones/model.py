# 
import peewee
import components

from tags.model import Tag
from categories.model import Category

class Milestone(components.BaseDocumentModel):
    title = peewee.TextField()
    description = peewee.TextField()
    due_date = peewee.DateTimeField(null=True, default=None)
    tags = peewee.ManyToManyField(Tag)
    category = peewee.ForeignKeyField(Category, null=True, default=None)
    pass

TaggedMilestone = Milestone.tags.get_through_model()
