# coding=utf-8
import logging
import os
import sys
import inspect


PRODUCTION = (os.getenv("NOTES_PRODUCTION") == 'True')
DEBUG = (os.getenv("NOTES_DEBUG") == 'True')

logging.basicConfig(
    format='%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s') 
logging.getLogger().setLevel(logging.DEBUG if DEBUG else logging.INFO)
logging.disable(logging.NOTSET)
logging.info('Loading %s, app version = %s', __name__, os.getenv('CURRENT_VERSION_ID'))


# ---
# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


from components import MyJsonEncoder


class MyConfig(object):
    RESTFUL_JSON = {'cls': MyJsonEncoder}

    @staticmethod
    def init_app(app):
        import settings
        app.config.from_object(settings)
        config = "settings.production" if PRODUCTION else "settings.local"
        import importlib
        try:
            cfg = importlib.import_module(config)
            logging.info("Loaded %s" % config)
            app.config.from_object(cfg)
            # app.config['DEBUG'] = DEBUG
        except ImportError:
            logging.warning("Local settings module not found: %s", config)


from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
app.config.from_object(MyConfig)
MyConfig.init_app(app)
api = Api(app)


# ---

import components
import tasks
import notes 
import tags
import categories

models = []
tasks.init(app, api, models)
notes.init(app, api, models)
tags.init(app, api, models)
categories.init(app, api, models)

components.database_init(app, models)
