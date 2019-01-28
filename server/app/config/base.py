# coding=utf-8

import os

SRC_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SECRET_KEY = "write_something_here"
FLASH_MESSAGES = True

DATABASE = "sqlite"
DATABASE_NAME = "cai-notes"
DATABASE_PATH = "./app.db"

# Application in-dev. settings
TESTING = False
DEBUG = True

# LOGIN_DISABLED = True

# Set secret keys for CSRF protection
CSRF_SESSION_KEY = "write_something_nice_here"
CSRF_ENABLED = True
