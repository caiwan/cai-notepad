# coding=utf-8
import os
import json
import bcrypt

CONFIG_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# This is a Big No.
SECRET_KEY = None
try:
    with open(os.path.join(CONFIG_DIR, "app.secret")) as f:
        config = json.load(f)
        SECRET_KEY = config["secret"].encode("utf-8")
except:
    with open(os.path.join(CONFIG_DIR, "app.secret"), "w") as f:
        SECRET_KEY = bcrypt.gensalt()
        json.dump({"secret": SECRET_KEY.decode("utf-8")}, f)
    pass

if not SECRET_KEY:
    raise RuntimeError("Could not load / generate secret key")

FLASH_MESSAGES = True

DATABASE = os.getenv("DATABASE")
DATABASE_NAME = os.getenv("DATABASE_NAME", default="")
DATABASE_PATH = os.getenv("DATABASE_PATH", default="")
DATABASE_AUTH = {
    # "dbname": os.getenv("DATABASE_NAME", default=""),
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "host": os.getenv("DATABASE_HOST", default="127.0.0.1"),
    "port": int(os.getenv("DATABASE_PORT", default=5432))
}

# Application in-dev. settings
TESTING = False
DEBUG = False

# LOGIN_DISABLED = True

# Set secret keys for CSRF protection
CSRF_SESSION_KEY = os.getenv("CSRF_SESSION_KEY", "")
CSRF_ENABLED = os.getenv("CSRF_SESSION_KEY") is not None or len(str(os.getenv("CSRF_SESSION_KEY")))

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
