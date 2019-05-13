# coding=utf-8

import os

SRC_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Generate it with manage.py gensalt. You should get something like this:
SECRET_KEY = b'$2b$12$4KQgT9MsGuHCQ2i3aA05Cu'
FLASH_MESSAGES = True

DATABASE = "sqlite"
DATABASE_NAME = "cai-notes"
DATABASE_PATH = "./app.db"
# -- OR --
DATABASE = "postgresql"
DATABASE_NAME = "notesapp"
DATABASE_AUTH = {
    "user": "notesappuser",
    "password": "notespassword",
    "host": "127.0.0.1",
    "port": 5432
}

# Application in-dev. settings
TESTING = False
DEBUG = True

# LOGIN_DISABLED = True

# Set secret keys for CSRF protection
CSRF_SESSION_KEY = "qWmODTwKC95EpJHp5zmW7Ui9DkraYLUa"
CSRF_ENABLED = True

APP_INTEGRATIONS = {
    "oauth-google": {
        "enabled": False,
        "client_id": "<client_id>",
        "client_secret": "<client_secret>",
        "scope": "profile email",
    },
    "oauth-twitter": {
        "enabled": False,
    },
    "oauth-habitica": {
        "enabled": False,
    },
}
