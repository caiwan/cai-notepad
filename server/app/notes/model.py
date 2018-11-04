import mongoengine
import components

from tags.model import Tag
# from categories.model import Category

class Note(components.BaseModel):
    title = mongoengine.StringField(max_length=512)
    content = mongoengine.StringField()
    is_archived = mongoengine.BooleanField(default=False)
    is_pinned = mongoengine.BooleanField(default=False)
    tags = mongoengine.ListField(mongoengine.ReferenceField(Tag), default=[])
    # category = mongoengine.ReferenceField(Category, default=None)
    # tasks = 
    # due_date = ?
    # milestone = ? 
    # decoration = ? (like colors, etc)

# Other type of notes and its extensions goez here
