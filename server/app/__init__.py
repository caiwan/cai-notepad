# coding=utf-8

import logging
import os, sys
import importlib
import base64

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

import app.components
from app.user import loginService

# modules
MODULES = [
    "user",
    "user.settings",
    # "user.admin"
    "notes",
    "notes.attachments",
    "tags",
    "tasks",
    "categories",
    "milestones",
    "worklog"
]


PRODUCTION = (os.getenv("FLASK_ENV") == "production")
DEBUG = (os.getenv("FLASK_DEBUG") == "True")
TESTING = (os.getenv("FLASK_TESTING") == "True")

logging.basicConfig(
    format="%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s")
logging.getLogger().setLevel(logging.DEBUG if DEBUG and not TESTING else logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG if DEBUG else logging.INFO)
logging.disable(logging.NOTSET)
logging.info("Loading %s, app version = %s", __name__,
             os.getenv("CURRENT_VERSION_ID"))

# ---
# fix import paths for internal imports
APP_ROOT = os.path.dirname(__file__)


class MyConfig(object):
    RESTFUL_JSON = {
        "cls": app.components.MyJsonEncoder,
        "indent": 0 if PRODUCTION else 2
    }

    @staticmethod
    def init_app(flask_app):
        import config
        flask_app.config.from_object(config)
        if APP_ROOT not in sys.path:
            sys.path.insert(0, APP_ROOT)
        config = "config.production" if PRODUCTION else "config.local"
        try:
            cfg = importlib.import_module(config)
            logging.info("Loaded %s" % config)
            flask_app.config.from_object(cfg)
        except ImportError:
            logging.warning("Local settings module not found: %s", config)


# --- Initialize Flask
APP = Flask(__name__)
APP.config.from_object(MyConfig)
MyConfig.init_app(APP)
API = Api(APP)
CORS = CORS(APP)

# --- Initialize Application

MODELS = []
SETTINGS = {}

for module in MODULES:
    try:
        module = importlib.import_module("app." + module)
        logging.info("Loaded %s" % module.__name__)
        module.module.register(
            app=APP,
            api=API,
            models=MODELS,
            settings=SETTINGS,
            cors=CORS,
        )
    except ImportError:
        logging.error("Module not found  %s", module)


if not TESTING:
    app.components.database_init(APP, MODELS)
    app.components.database_connect()
