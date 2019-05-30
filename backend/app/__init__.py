# coding=utf-8

import logging
import os
import sys
import importlib

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from flask_principal import PermissionDenied

import app.components
import app.auth
import app.settings

# modules
MODULES = [
    "settings",
    "user",
    "user.oauth",
    "user.settings",
    "notes",
    "notes.attachments",
    "sync",
    "tags",
    "tasks",
    "categories",
    # "milestones",
    # "worklog"
]

ENVIRONMENT = os.getenv("FLASK_ENV", default="production")
PRODUCTION = (os.getenv("FLASK_ENV", default="production") == "production")
TEST = (os.getenv("FLASK_ENV", default="production") == "test")
DEBUG = (os.getenv("FLASK_DEBUG", default="False") == "True")

logging.disable(logging.NOTSET)
if not PRODUCTION:
    logging.basicConfig(format="%(levelname)-7s %(module)s.%(funcName)s - %(message)s")
    logging.getLogger().setLevel(logging.DEBUG if DEBUG and not TEST else logging.INFO)
else:
    logging.basicConfig(format="%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s")
    logging.getLogger().setLevel(logging.INFO) # ? Isn't it enough?

logging.info("Loading %s, app version = %s", __name__,
             os.getenv("CURRENT_VERSION_ID"))


# ---
# add import paths for internal imports
APP_ROOT = os.path.dirname(__file__)


class MyConfig(object):
    RESTFUL_JSON = {
        "cls": app.components.MyJsonEncoder,
        "indent": 0 if PRODUCTION else 2,
        "sort_keys": False
    }

    @staticmethod
    def init_app(flask_app):
        import config
        flask_app.config.from_object(config)
        if APP_ROOT not in sys.path:
            sys.path.insert(0, os.path.dirname(APP_ROOT + "/../"))

        # config = "config.production" if PRODUCTION else "config.local"
        # config = "config.test" if TEST else config
        config = "config.%s" % ENVIRONMENT
        try:
            cfg = importlib.import_module(config)
            logging.info("Loaded %s" % config)
            flask_app.config.from_object(cfg)
        except ImportError:
            logging.warning("Local settings module not found: %s", config)


# --- Initialize Flask
APP = Flask(__name__, static_url_path=None)
APP.config.from_object(MyConfig)
MyConfig.init_app(APP)
API = Api(APP)
CORS = CORS(APP)

app.auth.principal.init_app(APP)

# setup all the message handlers
@app.auth.error_handler
def auth_error_callback():
    return app.components.error_handler(app.components.NoPermissionError())


@APP.errorhandler(PermissionDenied)
def handle_http_error(e):
    return app.components.error_handler(app.components.NoPermissionError())


@APP.errorhandler(Exception)
def handle_error(e):
    if not isinstance(e, app.components.BaseHTTPException) and not PRODUCTION:
        # raise e
        logging.exception(str(e))
    return app.components.error_handler(e)


@APP.errorhandler(404)
def handle_base_error(e):
    return app.components.error_handler(app.components.ResourceNotFoundError())


# --- Initialize Application
MODELS = []
SETTINGS = {
    "csrftoken": "",
    "root": "./api"
}

for module in MODULES:
    try:
        module = importlib.import_module("app." + module)
        logging.info("Loaded %s" % module.__name__)
        module.module.register(
            app=APP,
            api=API,
            models=MODELS,
            settings=SETTINGS,
        )
    except ImportError:
        logging.error("Module not found %s", module)
        raise

app.settings.settingsService.set_settings(SETTINGS)

if not TEST:
    app.components.database_init(APP, MODELS)
    app.components.database_connect()
