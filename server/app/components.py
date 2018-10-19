import logging
import inspect
import os
import sys
import inspect

import logging
import json

from datetime import datetime

from flask_mongoengine import MongoEngine
import mongoengine

from flask_restful import Resource

# -- Controller

BASE_PATH = "/api"


class Controller(Resource):
    path = ""


class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, mongoengine.fields.ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return int(obj.strftime('%s'))
        return json.JSONEncoder.default(self, obj)


# --- Database


DB = MongoEngine()


class BaseModel(mongoengine.DynamicDocument):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    created = mongoengine.DateTimeField(default=datetime.now)
    edited = mongoengine.DateTimeField(default=datetime.now)
    is_deleted = mongoengine.BooleanField(default=False)

    @staticmethod
    def update_document(document, data_dict):

        def field_value(field, value):

            if field.__class__ in (
                mongoengine.fields.ListField, 
                mongoengine.fields.SortedListField
            ):
                return [
                    field_value(field.field, item)
                    for item in value
                ]

            if field.__class__ in (
                mongoengine.fields.EmbeddedDocumentField,
                mongoengine.fields.GenericEmbeddedDocumentField,
                mongoengine.fields.ReferenceField,
                mongoengine.fields.GenericReferenceField
            ):
                return field.document_type(**value)

            if field.__class__ in (
                mongoengine.fields.DateTimeField,
                mongoengine.fields.ComplexDateTimeField,
            ):
                return datetime.utcfromtimestamp(int(value)) # field.__class__(datetime.utcfromtimestamp(int(**value)))

            return value

        [setattr(
            document, key,
            field_value(document._fields[key], value)
        ) for key, value in data_dict.items()]

        return document


# --- Register class tools

def register_controllers(api, controllers):
    for clazz in controllers:
        path = BASE_PATH + clazz.path
        logging.info("Register endpoint {} {}".format(path, clazz.__name__))
        api.add_resource(clazz, path)
    pass


def database_init(app):
    DB.init_app(app)
    pass
