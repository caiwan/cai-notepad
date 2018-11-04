import mongoengine

class Tag(mongoengine.Document):
    tag = mongoengine.StringField(primary_key=True, max_length=128)

class FuzzyTag(mongoengine.Document):
    tag = mongoengine.ReferenceField(Tag, required=True)
    fuzzy = mongoengine.StringField(required=True, max_length=128)
