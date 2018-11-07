import mongoengine
import components

class Category(components.BaseModel):
    title = mongoengine.StringField(max_length=512)
    parent = mongoengine.ReferenceField('self', default=None)
    children = mongoengine.ListField(mongoengine.ReferenceField('self'), default=[])
    is_archived = mongoengine.BooleanField(default=False)
    is_protected = mongoengine.BooleanField(defalt=False)
    order = mongoengine.IntField(default=0)
    # ... 
    # decoration = ? like colors, meta etc
