# coding=utf-8

import logging
import os, sys

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

import app.components

# modules
import app.tasks
import app.notes
import app.tags
import app.milestones


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
# if APP_ROOT not in sys.path:
#     sys.path.insert(0, APP_ROOT)


class MyConfig(object):
    RESTFUL_JSON = {
        "cls": app.components.MyJsonEncoder,
        "indent": 0 if PRODUCTION else 2
    }

    @staticmethod
    def init_app(flask_app):
        import app.config
        flask_app.config.from_object(app.config)
        if APP_ROOT not in sys.path:
            sys.path.insert(0, APP_ROOT)
        config = "config.production" if PRODUCTION else "config.local"
        import importlib
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
CORS(APP)

# --- Initialize Application

MODELS = []

app.notes.init(APP, API, MODELS)
app.tags.init(APP, API, MODELS)
app.categories.init(APP, API, MODELS)
app.tasks.init(APP, API, MODELS)

if not TESTING:
    app.components.database_init(APP, MODELS)
    app.components.database_connect()
