# coding=utf-8
import logging
import os
import sys
import inspect

logging.basicConfig(
    format='%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.info('Loading %s, app version = %s', __name__, os.getenv('CURRENT_VERSION_ID'))

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


PRODUCTION = __name__ != "__main__"
DEBUG = not PRODUCTION


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
            logging.debug("Loaded %s" % config)
            app.config.from_object(cfg)
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

components.database_init(app)

models = []
tasks.init(app, api, models)


# --- start dev server

# if app.debug and __name__ != '__main__':
#     from werkzeug.debug import DebuggedApplication
#     app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

if __name__ == '__main__':
    logging.debug("PRODUCTION: %s" % PRODUCTION)
    logging.debug("app.debug: %s" % app.debug)
    logging.debug("app.testing: %s" % app.testing)

    app.run(host="0.0.0.0", port=5000)
