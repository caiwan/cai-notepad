import logging
import os, sys

import json

from datetime import datetime

from flask_mongoengine import MongoEngine
import mongoengine

from flask_restful import Resource


# -- Service


class Service:
    _model_class = None
    
    def fetch_all_items(self):
        assert self._model_class
        return self._model_class.objects(is_deleted=False).order_by('-edited')

    def read_item(self, item_id):
        assert self._model_class
        return self._model_class.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)

    def create_item(self, item_json):
        assert self._model_class        
        item = BaseModel.update_document(self._model_class(), item_json)
        item.save()
        return item

    def update_item(self, item_id, item_json):
        assert self._model_class        
        item = self._model_class.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
        BaseModel.update_document(item, item_json)
        item.changed()
        item.save()
        return item

    def delete_item(self, item_id):
        assert self._model_class
        item = self._model_class.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
        item.is_deleted = True
        item.changed()
        item.save()

    def serialize_item(self, item):
        return item.to_mongo()


# -- Controller

BASE_PATH = "/api"

class Controller(Resource):
    path = ""
    _service = None

    def get(self):
        return({"error": ['Not implemented']}, 501)

    def post(self):
        return({"error": ['Not implemented']}, 501)

    def put(self):
        return({"error": ['Invalid method call or not implemented']}, 405)

    def delete(self):
        return({"error": ['Invalid method call or not implemented']}, 405)

    def patch(self):
        return({"error": ['Invalid method call or not implemented']}, 405)

    def _get_cls(self):
        assert self._service
        assert self._service._model_class
        return self._service._model_class

    # -- BASIC CRUD implementations for rapid prototyping
    def _fetch_all(self, *args, **kwargs):
        assert self._service
        try:
            items_json = [self._service.serialize_item(item) for item in self._service.fetch_all_items(*args, **kwargs)]
            return(items_json, 200)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)
        # except Exception as e:
        #     logging.error("Excpetion: " + str(e))
        #     return({"error": [str(e)]}, 500)   


    def _create(self, item_json, *args, **kwargs):
        assert self._service
        if '_id' in item_json:
            del item_json['_id']
        try: 
            return (self._service.serialize_item(self._service.create_item(item_json, *args, **kwargs)), 201)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)
        # except Exception as e:
        #     logging.error("Excpetion: " + str(e))
        #     return({"error": [str(e)]}, 500)   

    def _read(self, item_id, *args, **kwargs):
        _cls = self._get_cls()
        try:
            return (self._service.serialize_item(self._service.read_item(item_id, *args, **kwargs)), 200)
        except _cls.DoesNotExist as e:
            return({"error": [str(e)]}, 404)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)
        # except Exception as e:
        #     logging.error("Excpetion: " + str(e))
        #     return({"error": [str(e)]}, 500)

        return({"error": ["FATAL: you should not be able to see this"]}, 500)

    def _update(self, item_id, item_json, *args, **kwargs):
        _cls = self._get_cls()
        if '_id' in item_json:
            del item_json['_id']
        try:
            return (self._service.serialize_item(self._service.update_item(item_id, item_json, *args, **kwargs)), 200)
        except _cls.DoesNotExist as e:
            return({"error": str(e)}, 404)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)
        # except Exception as e:
        #     logging.error("Excpetion: " + str(e))
        #     return({"error": [str(e)]}, 500)

        return({"error": ["FATAL: you should not be able to see this"]}, 500)

    def _delete(self, item_id, *args, **kwargs):
        _cls = self._get_cls()
        try:
            self._service.delete_item(item_id, *args, **kwargs)
        except _cls.DoesNotExist as e:
            return({"error": [str(e)]}, 404)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)
        # except Exception as e:
        #     logging.error("Excpetion: " + str(e))
        #     return({"error": [str(e)]}, 500)
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
                if value:
                    return field.document_type(**value)
                return field.document_type()


            if field.__class__ in (
                mongoengine.fields.DateTimeField,
                mongoengine.fields.ComplexDateTimeField,
            ):
                # field.__class__(datetime.utcfromtimestamp(int(**value)))
                return datetime.utcfromtimestamp(int(value))

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
    # models are unnesesarry, however it's nesesarry for dump/import db or backup
    DB.init_app(app)
    pass
