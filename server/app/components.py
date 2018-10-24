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

    # -- BASIC CRUD implementations for rapid prototyping
    def _fetch_all(self, _cls):
        items_json = [item.to_mongo() for item in _cls.objects(is_deleted=False)]
        return(items_json, 200)


    def _create(self, _cls, _request):
        item_json = _request.json
        if '_id' in item_json:
            del item_json['_id']

        item = BaseModel.update_document(_cls(), item_json)
        item.save()
        return (item.to_mongo(), 201)


    def _read(self, _cls, item_id):
        try: 
            item = _cls.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
            return (item.to_mongo(), 200)

        except _cls.DoesNotExist as e:
            return({"error" : [str(e)]}, 404)
        except e:
            return({"error" : [str(e)]}, 500)

        return({"error" : ["FATAL: you should not be able to see this"]}, 500)


    def _update(self, _cls, _request, item_id):
        item_json = _request.json
        if '_id' in item_json:
            del item_json['_id']
        try: 
            item = _cls.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
            BaseModel.update_document(item, item_json)
            item.changed()
            item.save()
            return (item.to_mongo(), 200)

        except _cls.DoesNotExist as e:
            return({"error" : str(e)}, 404)

        except :
            return({
                "error" : [str(err) for err in sys.exc_info()]
            }, 500)

        return({"error" : ["FATAL: you should not be able to see this"]}, 500)
        

    def _delete(self, _cls, item_id):
        try: 
            item = _cls.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
            item.is_deleted = True
            item.changed()
            item.save()
        except _cls.DoesNotExist as e:
            return({"error" : [str(e)]}, 404)
        except e:
            return({"error" : [str(e)]}, 500)

        return ('', 201)



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

    def changed(self):
        self.edited = datetime.now()

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


def database_init(app, models):
    DB.init_app(app)
    pass
