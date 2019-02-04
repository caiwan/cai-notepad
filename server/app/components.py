import logging

import json
from datetime import datetime, date

import peewee
from playhouse.shortcuts import Proxy
from playhouse.shortcuts import dict_to_model, model_to_dict

from flask_restful import Resource

BASE_PATH = "/api"


class Service:
    """ Base service class
    """
    name = ""
    model_class = None
    settings = {}

    def fetch_all_items(self):
        assert self.model_class
        return self.model_class.select().where(self.model_class.is_deleted == False).objects()

    def read_item(self, item_id):
        assert self.model_class
        item = self.model_class.get(self.model_class.id == item_id, self.model_class.is_deleted == False)
        if not item:
            raise peewee.DoesNotExist()
        return item

    def create_item(self, item_json):
        assert self.model_class
        item = dict_to_model(self.model_class, item_json)
        item.save()
        return item

    def update_item(self, item_id, item_json):
        assert self.model_class
        my_item = self.model_class.select().where(self.model_class.id == item_id,
                                                  self.model_class.is_deleted == False).get()
        if my_item:
            item = dict_to_model(self.model_class, item_json)
            item.id = my_item.id
            item.changed()
            item.save()
            return item
        raise self.model_class.DoesNotExist()

    def delete_item(self, item_id):
        assert self.model_class
        my_item = self.model_class.select().where(self.model_class.id == item_id,
                                                  self.model_class.is_deleted == False).get()
        if my_item:
            my_item.is_deleted = True
            my_item.changed()
            my_item.save()
            return my_item
        raise peewee.DoesNotExist()

    def serialize_item(self, item):
        try:
            item_json = model_to_dict(item, exclude=["is_deleted"])
            del item_json["is_deleted"]  # Exclude does nothing :(
            return item_json
        except:
            logging.exception(str(item))
            raise

    def sanitize_fields(self, item_json):
        if "id" in item_json:
            del item_json["id"]
        # if 'uuid' in item_json:
            # del item_json['uuid']
        return item_json


# -- Controller
class Controller(Resource):
    """ Base controller Class
    """
    path = ""
    _service = None

    def get(self):
        return({"error": ["Not implemented"]}, 501)

    def post(self):
        return({"error": ["Not implemented"]}, 501)

    def put(self):
        return({"error": ["Invalid method call or not implemented"]}, 405)

    def delete(self):
        return({"error": ["Invalid method call or not implemented"]}, 405)

    def patch(self):
        return({"error": ["Invalid method call or not implemented"]}, 405)

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
            msg = "Bad request: " + str(e)
            logging.exception(msg)
            return({"error": [msg]}, 400)

    def _create(self, item_json, *args, **kwargs):
        assert self._service
        if "_id" in item_json:
            del item_json["_id"]
        try:
            return (self._service.serialize_item(self._service.create_item(item_json, *args, **kwargs)), 201)
        except RuntimeError as e:
            msg = "Bad request: " + str(e)
            logging.exception(msg)
            return({"error": [msg]}, 400)

    def _read(self, item_id, *args, **kwargs):
        _cls = self._get_cls()
        try:
            return (self._service.serialize_item(self._service.read_item(item_id, *args, **kwargs)), 200)
        except _cls.DoesNotExist as e:
            # logging.exception(item_id)
            return({"error": [str(e)]}, 404)
        except RuntimeError as e:
            msg = "Bad request: " + str(e)
            logging.exception(msg)
            return({"error": [msg]}, 400)

    def _update(self, item_id, item_json, *args, **kwargs):
        _cls = self._get_cls()
        if "_id" in item_json:
            del item_json["_id"]
        try:
            return (self._service.serialize_item(self._service.update_item(item_id, item_json, *args, **kwargs)), 200)
        except _cls.DoesNotExist as e:
            # logging.exception(" :".join(item_id, item_json))
            return({"error": str(e)}, 404)
        except RuntimeError as e:
            msg = "Bad request: " + str(e)
            logging.exception(msg)
            return({"error": [msg]}, 400)

    def _delete(self, item_id, *args, **kwargs):
        _cls = self._get_cls()
        try:
            self._service.delete_item(item_id, *args, **kwargs)
        except _cls.DoesNotExist as e:
            return({"error": [str(e)]}, 404)
        except RuntimeError as e:
            msg = "Bad request: " + str(e)
            logging.exception(msg)
            return({"error": [msg]}, 400)

        return ("", 200)


#
class MyJsonEncoder(json.JSONEncoder):
    """ Custom JSON enoder for certatin type of objects
    """

    def default(self, obj):
        # if isinstance(obj, mongoengine.fields.ObjectId):
            # return str(obj)
        if isinstance(obj, date):
            return int(obj.strftime("%s"))
        if isinstance(obj, datetime):
            return int(obj.strftime("%s"))
        return json.JSONEncoder.default(self, obj)


# Database

DB = Proxy()


class BaseModel(peewee.Model):
    """ Peewee's Base model
    """
    class Meta:
        database = DB


class BaseUser(BaseModel):
    """ Base model for user permissions
    """
    name = peewee.TextField()
    pass


class BaseRole(BaseModel):
    """ Base model for user roles
    """
    name = peewee.TextField()
    pass


class BaseDocumentRole(BaseModel):
    """ Access level management for each accessed role
    Such as read, write, manage, etc...
    """
    role = peewee.ForeignKeyField(BaseRole)
    access = peewee.TextField()


class BaseDocumentModel(BaseModel):
    """ Base model for document handling
    w/ extra fields built-in
    """
    created = peewee.DateTimeField(null=False, default=datetime.now)
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True)
    is_deleted = peewee.BooleanField(null=False, default=False)

    owner = peewee.ForeignKeyField(BaseUser)
    role = peewee.ForeignKeyField(BaseDocumentRole)

    def changed(self):
        self.edited = datetime.now()


# --- Register class tools
def register_controllers(api, controllers):
    for clazz in controllers:
        path = BASE_PATH + clazz.path
        logging.info("Register endpoint {} {}".format(path, clazz.__name__))
        api.add_resource(clazz, path)
    pass


def database_init(app, models):
    logging.debug("ConnectDB: " + app.config["DATABASE"])
    if app.config["DATABASE"] == "postgresql":
        from playhouse.pool import PooledPostgresqlExtDatabase
        database = PooledPostgresqlExtDatabase(
            app.config["DATABASE_NAME"], max_connections=16, stale_timeout=300, **app.config["DATABASE_AUTH"])

    elif app.config["DATABASE"] == "sqlite":
        from playhouse.pool import PooledSqliteDatabase
        database = PooledSqliteDatabase(app.config["DATABASE_PATH"], pragmas=(
            ("journal_mode", "wal"), ("cache_size", -1024 * 64)))

    else:
        raise RuntimeError("No database set or invalid")

    DB.initialize(database)


def database_connect():
    DB.connect()


def create_tables(app, models):
    DB.create_tables(models, safe=True)


# Module descriptor

class Module:
    """ Base module class
    """
    name = ""
    services = []
    models = []
    controls = []

    __is_initialized = False

    def pre_register(self, app, api, models, settings):
        """ A custom callback before register module
        """
        pass

    def post_register(self, app, api, models, settings):
        """ A custom callback after register a module
        """
        pass

    def register(self, app, api, models, settings):
        if settings is None:
            settings = {}
        if models is None:
            models = []

        self.pre_register(app, api, models, settings)

        if not self.__is_initialized:
            logging.info("=== Register module: {}".format(self.name))

            for model in self.models:
                logging.info("Register model {}".format(model.__name__))
                models.append(model)
                pass

            for service in self.services:
                logging.info("Register service {}".format(service.name))
                if service.name and service.settings:
                    settings[service.name] = service.settings.copy()

            for controller in self.controls:
                path = BASE_PATH + controller.path
                logging.info("Register endpoint {} {}".format(path, controller.__name__))
                api.add_resource(controller, path)
                pass

            # logging.info("\n")

            self.__is_initialized = True
            pass

        self.post_register(app, api, models, settings)

        pass
