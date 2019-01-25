import logging
import os
import sys

import json
import uuid

from datetime import datetime

import peewee
from playhouse.shortcuts import *
from playhouse.pool import *

from flask_restful import Resource


# -- Service


class Service:
    _model_class = None

    def fetch_all_items(self):
        assert self._model_class
        return self._model_class.select().where(self._model_class.is_deleted == False)

    def read_item(self, item_id):
        assert self._model_class
        item = self._model_class.select().where(self._model_class.id == item_id,
                                                self._model_class.is_deleted == False).get()
        if not item:
            raise peewee.DoesNotExist()
        return item

    def create_item(self, item_json):
        assert self._model_class
        item = dict_to_model(self._model_class, item_json)
        item.save(force_insert=True)
        return item

    def update_item(self, item_id, item_json):
        assert self._model_class
        my_item = self._model_class.select().where(self._model_class.id == item_id,
                                                   self._model_class.is_deleted == False).get()
        if my_item:
            item = dict_to_model(self._model_class, item_json)
            item.id = my_item.id
            item.changed()
            item.save()
            return item
        raise self._model_class.DoesNotExist()

    def delete_item(self, item_id):
        assert self._model_class
        my_item = self._model_class.select().where(self._model_class.id == item_id,
                                                   self._model_class.is_deleted == False).get()
        if my_item:
            my_item.is_deleted = True
            my_item.changed()
            my_item.save()
            return my_item
        raise peewee.DoesNotExist()

    def serialize_item(self, item):
        return model_to_dict(item)

    def sanitize_fields(self, item_json):
        if 'id' in item_json:
            del item_json['id']
        # if 'uuid' in item_json:
            # del item_json['uuid']
        return item_json



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
            items_json = [self._service.serialize_item(
                item) for item in self._service.fetch_all_items(*args, **kwargs)]
            return(items_json, 200)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)

    def _create(self, item_json, *args, **kwargs):
        assert self._service
        item_json = self._service.sanitize_fields(item_json)
        try:
            return (self._service.serialize_item(self._service.create_item(item_json, *args, **kwargs)), 201)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)

    def _read(self, item_id, *args, **kwargs):
        _cls = self._get_cls()
        try:
            return (self._service.serialize_item(self._service.read_item(item_id, *args, **kwargs)), 200)
        except _cls.DoesNotExist as e:
            return({"error": [str(e)]}, 404)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)

        return({"error": ["FATAL: you should not be able to see this"]}, 500)

    def _update(self, item_id, item_json, *args, **kwargs):
        _cls = self._get_cls()
        item_json = self._service.sanitize_fields(item_json)
        try:
            return (self._service.serialize_item(self._service.update_item(item_id, item_json, *args, **kwargs)), 200)
        except _cls.DoesNotExist as e:
            return({"error": str(e)}, 404)
        except RuntimeError as e:
            logging.info("Bad request: " + str(e))
            return(items_json, 400)

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
        return ('', 200)


class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj.hex)
        if isinstance(obj, datetime):
            return int(obj.strftime('%s'))
        return json.JSONEncoder.default(self, obj)


# --- Database

DB = Proxy()


class BaseModel(Model):
    class Meta:
        database = DB


class BaseDocumentModel(BaseModel):
    class Meta:
        database = DB
        # primary_key = peewee.UUIDField(default=uuid.uuid4)

    # id = peewee.UUIDField(primary_key=True, default=uuid.uuid4)
    created = peewee.DateTimeField(null=False, default=datetime.now)
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)
    is_deleted = peewee.BooleanField(null=False, default=False)

    def changed(self):
        self.edited = datetime.now()

# --- Register class tools


def register_controllers(api, controllers):
    for clazz in controllers:
        if not clazz.path:
            raise RuntimeError("Path is none or empty" + clazz.__name__)
        path = BASE_PATH + clazz.path
        logging.info("Register endpoint {} {}".format(path, clazz.__name__))
        api.add_resource(clazz, path)
    pass


def database_init(app, models):
    logging.debug("ConnectDB: " + app.config["DATABASE"])
    if app.config["DATABASE"] == "postgresql":
        database = PooledPostgresqlExtDatabase(
            app.config["DATABASE_NAME"], max_connections=16, stale_timeout=300, **app.config["DATABASE_AUTH"])

    elif app.config["DATABASE"] == "sqlite":
        database = SqliteDatabase(app.config["DATABASE_PATH"], pragmas=(
            ('journal_mode', 'wal'), ('cache_size', -1024 * 64)))

    else:
        raise RuntimeError("No database set or invalid")

    DB.initialize(database)



def database_connect():
    DB.connect()


def create_tables(app, models):
    DB.create_tables(models, safe=True)
