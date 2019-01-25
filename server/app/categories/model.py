import peewee
import components

class Category(components.BaseDocumentModel):
    title = peewee.TextField()
    is_archived = peewee.BooleanField(default=False)
    is_protected = peewee.BooleanField(default=False)
    order = peewee.IntegerField(default=0)
    spanning_order = peewee.IntegerField(default=0)
    parent = peewee.ForeignKeyField('self', backref='children', null=True)
    # ... 
    # decoration = ? like colors, meta etc
