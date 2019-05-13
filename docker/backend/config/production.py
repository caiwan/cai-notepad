# coding=utf-8
import os
import json

SRC_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Generate it with manage.py gensalt. You should get something like this:
SECRET_KEY = b"$2b$12$4KQgT9MsGuHCQ2i3aA05Cu"
with open("app.bootstrap") as f:
    config = json.load(f)
    SECRET_KEY = config["secret"].encode("utf-8")

FLASH_MESSAGES = True

DATABASE = os.environ["DATABASE"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_PATH = os.getenv("DATABASE_PATH")
DATABASE_AUTH = {
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "host": os.getenv("DATABASE_HOST", "127.0.0.1"),
    "port": int(os.getenv("DATABASE_PORT", 5432))
}

# Application in-dev. settings
TESTING = False
DEBUG = False

# LOGIN_DISABLED = True

# Set secret keys for CSRF protection
CSRF_SESSION_KEY = os.getenv("CSRF_SESSION_KEY", "")
CSRF_ENABLED = os.getenv("CSRF_SESSION_KEY") is not None or len(str(os.getenv("CSRF_SESSION_KEY")))

RESTFUL_JSON = {
    "indent": 0,
    "sort_keys": False
}

APP_INTEGRATIONS = {
    "oauth-google": {
        "enabled": os.getenv("GOOGLE_CLIENT_ID") is not None or len(str(os.getenv("GOOGLE_CLIENT_ID"))),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "scope": "profile email",
    },
    "oauth-twitter": {
        "enabled": False,
        # ...
    },
    "oauth-habitica": {
        "enabled": False,
        # ...
    },
}
