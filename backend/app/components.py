import logging

import json

from functools import wraps

from datetime import datetime, date
# import dateutil
from uuid import UUID

import peewee
from peewee import DatabaseProxy as Proxy
from playhouse.shortcuts import dict_to_model, model_to_dict

from peewee_migrate import Router

from flask_restful import Resource
from flask_restful import request

from flask import g


BASE_PATH = "/api"
not_found_message = "Requested resource does not exist on this server."
unauthorized_message = "User could not be authorized with the given credentials."
invalid_call_message = "This endpoint does not implements this method."
no_permission_message = "You don't have permission to access this resource on this server."

DB = Proxy()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Base DB models
class BaseModel(peewee.Model):
    """ Peewee's Base model
    """
    class Meta:
        database = DB


class BaseUser(BaseModel):
    """ Base model for user
    """
    class Meta:
        table_name = "users"  # 'user' is reserved in most of dbs
    name = peewee.TextField(null=False, index=True, unique=True)
    password = peewee.TextField(null=False)
    pass


class BaseRole(BaseModel):
    """ Base model for user roles
    """
    name = peewee.TextField(null=False, unique=True)
    pass


class BaseDocumentModel(BaseModel):
    """ Base model for document handling
    w/ extra fields built-in
    """
    created = peewee.DateTimeField(null=False, default=datetime.now, formats=["%s"])
    edited = peewee.DateTimeField(null=False, default=datetime.now, index=True, formats=["%s"])
    is_deleted = peewee.BooleanField(null=False, default=False)

    owner = peewee.ForeignKeyField(BaseUser, null=True)

    def changed(self):
        self.edited = datetime.now()

# Helpers


def current_user():
    if not hasattr(g, "current_user") or not g.current_user:
        return None
    else:
        return g.current_user


def current_user_id():
    if not hasattr(g, "current_user") or not g.current_user:
        return None
    else:
        return g.current_user.id


class BaseHTTPException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


class BadRequestError(BaseHTTPException):
    def __init__(self, payload=None):
        return BaseHTTPException.__init__(self, "Bad Request", payload=payload)


class MethodNotImplemented(BaseHTTPException):
    def __init__(self, payload=None):
        return BaseHTTPException.__init__(self, invalid_call_message, status_code=501, payload=payload)


class InvalidMethodCallError(BaseHTTPException):
    def __init__(self, payload=None):
        return BaseHTTPException.__init__(self, invalid_call_message, status_code=405, payload=payload)


class AuthorizationError(BaseHTTPException):
    def __init__(self, payload=None):
        return BaseHTTPException.__init__(self, unauthorized_message, status_code=401, payload=payload)


class NoPermissionError(BaseHTTPException):
    def __init__(self, payload=None):
        return BaseHTTPException.__init__(self, no_permission_message, status_code=403, payload=payload)


class ResourceNotFoundError(BaseHTTPException):
    def __init__(self, payload=None):
        return BaseHTTPException.__init__(self, not_found_message, status_code=404, payload=payload)


def error_handler(ex):
    if hasattr(ex, "to_dict") and hasattr(ex, "status_code"):
        return(json.dumps(ex.to_dict()), ex.status_code)
    elif isinstance(ex, Exception):
        return(json.dumps({"message": "Internal server error"}), 500)
    else:
        return(json.dumps({"message": "Bad request"}), 400)


class Service(metaclass=Singleton):
    """ Base service class
    """
    name = ""
    model_class = None
    settings = {}

    @DB.atomic()
    def fetch_all_items(self):
        assert self.model_class
        user_id = current_user_id()
        # TODO: opt out join w/ base user
        return self.model_class.select(
            self.model_class
        ).join(
            BaseUser, on=(self.model_class.owner == BaseUser.id)
        ).where(
            self.model_class.is_deleted == False,
            BaseUser.id == user_id
        ).objects()

    @DB.atomic()
    def read_item(self, item_id):
        assert self.model_class
        user_id = current_user_id()
        # This will raise not exist exception when not found anyways
        # TODO: opt out join w/ base user
        return self.model_class.select(
            self.model_class
        ).join(
            BaseUser, on=(self.model_class.owner == BaseUser.id)
        ).where(
            self.model_class.id == item_id,
            self.model_class.is_deleted == False,
            self.model_class.owner.id == user_id
        ).get()

    @DB.atomic()
    def create_item(self, item_json):
        assert self.model_class
        try:
            # TODO: opt out join w/ base user
            item = dict_to_model(
                self.model_class, self.sanitize_fields(item_json))
            item.owner = current_user()
            item.save()
            return item
        except Exception as ex:
            # DB.rollback()
            raise BadRequestError(payload={"reason": str(ex)})

    @DB.atomic()
    def update_item(self, item_id, item_json):
        assert self.model_class
        try:
            # TODO: opt out join w/ base user
            user_id = current_user_id()
            my_item = self.model_class.select(
                self.model_class
            ).join(
                BaseUser, on=(self.model_class.owner == BaseUser.id)
            ).where(
                self.model_class.id == item_id,
                self.model_class.is_deleted == False,
                self.model_class.owner.id == user_id
            ).get()

            item = dict_to_model(
                self.model_class, self.sanitize_fields(item_json)
            )
            item.id = my_item.id
            item.changed()
            # item.save(only=item.dirty_fields)
            item.save()
            return item
        except Exception as ex:
            # DB.rollback()
            raise BadRequestError(payload={"reason": str(ex)})

    @DB.atomic()
    def delete_item(self, item_id):
        assert self.model_class
        try:
            user_id = current_user_id()
            my_item = self.model_class.select(
                self.model_class
            ).join(
                BaseUser, on=(self.model_class.owner == BaseUser.id)
            ).where(
                self.model_class.id == item_id,
                self.model_class.is_deleted == False,
                self.model_class.owner.id == user_id
            ).get()
            my_item.is_deleted = True
            my_item.changed()
            my_item.save()
            # return my_item
        except Exception as ex:
            # DB.rollback()
            raise BadRequestError(payload={"reason": str(ex)})

    def serialize_item(self, item):
        item_json = model_to_dict(item, exclude=(
            self.model_class.is_deleted,
            self.model_class.owner
        ), recurse=False)
        return item_json

    # TODO: QnD hack, Remove this later on
    def sanitize_fields(self, item_json):
        logging.debug("Sanitize: %s" % str(item_json))
        if "id" in item_json:
            del item_json["id"]
        if "owner" in item_json:
            del item_json["owner"]
        if "user_id" in item_json:
            del item_json["user_id"]
        if "uuid" in item_json:
            del item_json["uuid"]
        if "children" in item_json:
            del item_json["children"]
        if "created" in item_json:
            item_json["created"] = datetime.fromtimestamp(int(item_json["created"]))
        if "edited" in item_json:
            item_json["edited"] = datetime.fromtimestamp(int(item_json["edited"]))
        return item_json


# -- Controller
class Controller(Resource):
    """ Base controller Class
    """
    path = ""
    _service = None

    def get(self):
        raise InvalidMethodCallError()

    def post(self):
        raise InvalidMethodCallError()

    def put(self):
        raise InvalidMethodCallError()

    def delete(self):
        raise InvalidMethodCallError()

    def patch(self):
        raise InvalidMethodCallError()

    def _get_cls(self):
        assert self._service
        assert self._service.model_class
        return self._service.model_class

    # -- BASIC CRUD implementations for rapid prototyping
    def _fetch_all(self, *args, **kwargs):
        assert self._service
        try:
            items_json = [
                self._service.serialize_item(item) for item in self._service.fetch_all_items(*args, **kwargs)
            ]
            return(items_json, 200)
        except RuntimeError as e:
            logging.exception(e)
            raise BadRequestError()

    def _create(self, item_json, *args, **kwargs):
        assert self._service
        if "_id" in item_json:
            del item_json["_id"]
        try:
            return (self._service.serialize_item(self._service.create_item(item_json, *args, **kwargs)), 201)
        except RuntimeError as e:
            logging.exception(e)
            raise

    def _read(self, item_id, *args, **kwargs):
        _cls = self._get_cls()
        try:
            return (self._service.serialize_item(self._service.read_item(item_id, *args, **kwargs)), 200)
        except _cls.DoesNotExist:
            raise ResourceNotFoundError()
        except RuntimeError as e:
            logging.exception(e)
            raise

    def _update(self, item_id, item_json, *args, **kwargs):
        _cls = self._get_cls()
        if "_id" in item_json:
            del item_json["_id"]
        try:
            return (self._service.serialize_item(self._service.update_item(item_id, item_json, *args, **kwargs)), 200)
        except _cls.DoesNotExist:
            raise ResourceNotFoundError()
        except RuntimeError as e:
            logging.exception(e)
            raise

    def _delete(self, item_id, *args, **kwargs):
        _cls = self._get_cls()
        try:
            self._service.delete_item(item_id, *args, **kwargs)
        except _cls.DoesNotExist:
            raise ResourceNotFoundError()
        except RuntimeError as e:
            logging.exception(e)
            raise

        return ("", 200)


class MyJsonEncoder(json.JSONEncoder, metaclass=Singleton):
    """ Custom JSON enoder for certatin type of objects
    """

    def default(self, obj):
        if callable(obj):
            return self.default(obj())
        if isinstance(obj, date):
            return int(obj.strftime("%s"))
        if isinstance(obj, datetime):
            return int(obj.strftime("%s"))
        if isinstance(obj, UUID):
            return str(obj)
        if type(obj) is bytes:
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)


# Register and connection tools
def register_controllers(api, controllers):
    for clazz in controllers:
        path = BASE_PATH + clazz.path
        logging.info("Register endpoint {} {}".format(path, clazz.__name__))
        api.add_resource(clazz, path)
    pass


def database_init(app, models):
    logging.info("Init database connection: %s %s" % (app.config["DATABASE"], app.config["DATABASE_NAME"]))
    if app.config["DATABASE"] == "postgresql":
        from playhouse.pool import PooledPostgresqlExtDatabase
        database = PooledPostgresqlExtDatabase(app.config["DATABASE_NAME"], max_connections=16, stale_timeout=300, **app.config["DATABASE_AUTH"])

    elif app.config["DATABASE"] == "sqlite":
        from playhouse.pool import PooledSqliteDatabase
        database = PooledSqliteDatabase(app.config["DATABASE_PATH"], pragmas={
            "journal_mode": "wal",
            "cache_size": -1024 * 64,
            "foreign_keys": 1
        })
    else:
        raise RuntimeError("No database set or invalid")
    try:
        DB.initialize(database)
    except:
        logging.exception("Could not initialize database")


def database_connect():
    try:
        DB.connect()
    except:
        logging.exception("Could not connect to database")


# Maintenance / testing stuff
def _create_tables(app, models):
    try:
        DB.create_tables(models, safe=True)
    except:
        logging.exception("Could not create tables")


def _drop_tables(app, models):
    try:
        DB.drop_tables(models, safe=True, cascade=True)
    except:
        logging.exception("Could not drop tables")


def _truncate_tables(app, models):
    try:
        for model in models:
            model.truncate_table(restart_identity=True, cascade=True)
    except:
        logging.exception("Could not truncate tables")


# Quick and dirty Object mapping
def _map(mapper, object):
    if not mapper:
        return object
    return mapper(object)
    pass


def object_mapping(request_mapper=None, response_mapper=None):
    def decorator_marshal(f):
        @wraps(f)
        def check_rx_tx_type(*args, **kwargs):
            payload = _map(request_mapper, request.json)
            result = f(payload, *args, **kwargs)
            response = result
            status = 200
            if isinstance(response, tuple):
                (response, status) = result
            response = _map(response_mapper, response)
            return (response, status)
        pass
    pass
    return decorator_marshal


# Maintenance tools
def _database_backup(models):
    backup = {}
    for model in models:
        records = model.select().objects()
        backup[model.__name__] = [model_to_dict(
            record, recurse=False) for record in records]
    return backup


def _database_restore(models, data):
    DB.drop_tables(models, safe=True)
    DB.create_tables(models, safe=True)
    model_map = dict((m.__name__, m) for m in models)
    with DB.atomic():
        # TODO: TBD
        # this doesn't work this way, because we'll need to insert all the FKs later some way
        # 1. Trim FKs
        # 2 ...
        # 3 ...
        for table, records in data.items():
            if records:
                model = model_map[table]
                model.insert_many(records).on_conflict_ignore(True).execute()
                logging.info("Restored db: %s" % (model.__name__))


def _createmigration(migration_name):
    router = Router(DB)
    router.create(migration_name)


def _runmigration(migration_name):
    router = Router(DB)
    router.run(migration_name)


def _rollbackmigration(migration_name):
    router = Router(DB)
    router.rollback(migration_name)


# Module descriptor
class Module(metaclass=Singleton):
    """ Base module class
    """
    name = ""
    services = []
    models = []
    controllers = []

    __is_initialized = False

    def pre_register(self, *args, **kwargs):
        """ A custom callback before register module
        """
        pass

    def post_register(self, *args, **kwargs):
        """ A custom callback after register a module
        """
        pass

    def register(self, *args, **kwargs):
        (api, models, settings) = (
            kwargs["api"], kwargs["models"], kwargs["settings"])

        if settings is None:
            settings = {}
        if models is None:
            models = []

        self.pre_register(*args, **kwargs)

        if not self.__is_initialized:
            logging.debug("=== Register module: {}".format(self.name))

            for model in self.models:
                logging.debug("Register model {}".format(model.__name__))
                models.append(model)
                pass

            for service in self.services:
                logging.debug("Register service {}".format(service.name))
                if service.name and service.settings:
                    settings[service.name] = service.settings.copy()

            for controller in self.controllers:
                path = BASE_PATH + controller.path
                logging.debug("Register endpoint {} {}".format(
                    path, controller.__name__))
                api.add_resource(controller, path, strict_slashes=False)
                pass

            self.__is_initialized = True
            pass

        self.post_register(*args, **kwargs)

        pass
