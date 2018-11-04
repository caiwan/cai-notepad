import mongoengine
import logging
import copy
from slugify import slugify 

class Tag(mongoengine.Document):
    slug = mongoengine.StringField(primary_key=True, max_length=128)
    tag = mongoengine.StringField(required=True, max_length=128)

class FuzzyTag(mongoengine.Document):
    pass
