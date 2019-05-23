#!/usr/bin/env
# coding=utf-8
from flask_script import Server, Manager

import os, sys
import json

from peewee_migrate import Router
from pathlib import Path


# add import paths for internal imports
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ModuleNotFoundError:
    pass


import app  # noqua: E402
from app import components  # noqua: E402
from app.components import DB  # noqua: E402
from app.auth import _adduser  # noqua: E402
from app.auth import _rmuser  # noqua: E402
from app.auth import _setuser  # noqua: E402
from app.auth import _assignrole  # noqua: E402
from app.auth import _revokerole  # noqua: E402
from app.auth import _listusers  # noqua: E402
from app.auth import _listuserroles  # noqua: E402
from app.auth import _listroles  # noqua: E402
from app.categories import _flatten_all_categories  # noqua: E402
from app.auth import _addrole, _adduser, _assignrole, _setuser  # noqua: E402


manager = Manager(app.APP)


# User management
@manager.command
def adduser(username, password):
    """Adds a new user"""
    _adduser(username, password)


@manager.command
def rmuser(user_id):
    """Removes an existing user"""
    _rmuser(user_id)


@manager.command
def setuser(user_id, key, value):
    """Sets a user"s credentials and other parameters"""
    _setuser(user_id, key, value)


@manager.command
def assignrole(user_id, role):
    """Adds a role to an user"""
    _assignrole(user_id, role)


@manager.command
def revokerole(user_id, role):
    """Revokes a role from a user"""
    _revokerole(user_id, role)


@manager.command
def listusers():
    """Lists all the existing users"""
    users = _listusers()
    print("{:<4} {:<32} {:<2} {:<2} {:<10} {:<10} {:<32}".format(
        "Id", "Name", "A", "D", "Created", "Edited", "Ref id"))
    for user in users:
        _df = "%s"
        user["user_ref_id"] = str(user["user_ref_id"])
        user["created"] = user["created"].strftime(_df)
        user["edited"] = user["edited"].strftime(_df)
        print("{id:<4} {name:<32} {is_active:<2} {is_deleted:<2} {created:<10} {edited:<10} {user_ref_id:<32}".format(**user))


@manager.command
def listuserroles(user_id):
    """Lists all the roles assigned to a user"""
    print(", ".join(p["name"] for p in _listuserroles(user_id)))
    pass


@manager.command
def listroles():
    """Lists all the existing roles"""
    roles = _listroles()
    print("{:<4} {:<32}".format("Id", "Name"))
    for role in roles:
        print("{id:<4} {name:<32}".format(**role))


# Database management
@manager.command
def createdb():
    """Creates the inital database schema and default users"""
    components.create_tables(app.APP, app.MODELS)

    # Quick and dirty way to add a default admin role and user
    from app.auth import _addrole, _adduser, _assignrole, _setuser
    roles = ["ADMIN"]  # ... add more if needed later
    for role in roles:
        _addrole(role)
    uid = _adduser("admin", "admin")
    _assignrole(uid, "admin")
    _setuser(uid, "is_active", "1")


@manager.command
def backupdb(filename):
    """Creates a backup from the database"""
    import json
    from app.components import MyJsonEncoder, _database_backup
    with open(filename, mode="w") as file:
        backup = _database_backup(app.MODELS)
        json.dump(backup, file, cls=MyJsonEncoder, indent=2)


@manager.command
def restoredb(filename):
    """Restores db from a backup"""
    from app.components import _database_restore
    with open(filename, mode="r") as file:
        backup = json.load(file)
        _database_restore(app.MODELS, backup)


@manager.command
def createmigration(migration_name):
    """Creates a migration script from the database"""
    router = Router(DB)
    router.create(migration_name)


@manager.command
def runmigration(migration_name):
    """Runs a migration script from the database"""
    router = Router(DB)
    router.run(migration_name)


@manager.command
def rollbackmigration(migration_name):
    """Rolls back a migration script from the database"""
    router = Router(DB)
    router.rollback(migration_name)


# Entity management
@manager.command
def flattencategories():
    """ Reorganizes and make catecory trees flatten for all users """
    _flatten_all_categories()


# Bootstrapping app for the first time
@manager.command
def bootstrap(migration_name, user, password):
    """Bootstraps the application for the first time"""

    router = Router(DB)
    router.run(migration_name)

    # Quick and dirty way to add a default admin role and user
    if not _listusers():
        roles = ["ADMIN"]  # ... add more if needed later
        for role in roles:
            _addrole(role)
        uid = _adduser(user, password)
        _assignrole(uid, "admin")
        _setuser(uid, "is_active", "1")


# override the default 127.0.0.1 binding address
manager.add_command("runserver", Server(host="0.0.0.0", use_reloader=False, port=5000))

if __name__ == "__main__":
    manager.run()
