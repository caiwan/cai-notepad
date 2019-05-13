import peewee

from app import components


class Category(components.BaseDocumentModel):
    name = peewee.TextField()
    comment = peewee.TextField(default="")
    is_archived = peewee.BooleanField(default=False)
    is_protected = peewee.BooleanField(default=False)
    order = peewee.IntegerField(default=0)
    path = peewee.TextField()
    parent = peewee.ForeignKeyField("self", backref="children", null=True)
