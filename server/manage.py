#!/usr/bin/env
# coding=utf-8
import logging
from flask_script import Server, Manager, Command
from dotenv import load_dotenv, find_dotenv
import os
import sys


# fix import paths for internal imports
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

load_dotenv(find_dotenv())

import app

manager = Manager(app.APP)


class CreateDb(Command):
    def run(self):
        from app import components
        components.create_tables(app.APP, app.MODELS)


class Runserver(Server):
    def run(self):
        self.__call__(app.APP,
                      self.port,
                      self.host,
                      self.use_debugger,
                      self.use_reloader,
                      self.threaded,
                      self.process,
                      self.passthrough_errors,
                      (self.ssl_crt, self.ssl_key)
                      )


@manager.command
def adduser(username, password):
    """Adds a new user"""
    from app.auth import _adduser
    user_id = _adduser(username, password)
    # print("Created: %d" % user_id)

@manager.command
def rmuser(user_id):
    """Removes an existing user"""
    from app.auth import _rmuser
    _rmuser(user_id)
    pass


@manager.command
@manager.option("-p", "--password", dest="password", default=None)
@manager.option("-a", "--active", dest="is_active", default=None)
@manager.option("-d", "--deleted", dest="is_deleted", default=None)
def setuser(user_id, *args, **kwargs):
    """Sets a user's credentials and other parameters"""
    pass


@manager.command
def assignrole(user_id, role):
    """Adds a role to an user"""
    pass


@manager.command
def revokerole(user_id, role):
    """Revokes a role from a user"""
    pass


@manager.command
def listusers():
    """Lists all the existing users"""
    from app.auth import _listusers
    users = _listusers()
    print("{:<4} {:<15} {:<2} {:<2} {:<10} {:<10} {:<32}".format(
        'Id', 'Name', 'A', 'D', 'Created', 'Edited', 'Ref id'))
    for user in users:
        _df = "%s"
        user["user_ref_id"] = str(user["user_ref_id"])
        user["created"] = user["created"].strftime(_df)
        user["edited"] = user["edited"].strftime(_df)
        print("{id:<4} {name:<15} {is_active:<2} {is_deleted:<2} {created:<10} {edited:<10} {user_ref_id:<32}".format(**user))


@manager.command
def listuserroles(user_id):
    """Lists all the roles assigned to a user"""
    pass


@manager.command
def listroles():
    """Lists all the existing roles"""
    from app.auth import _listroles
    roles = _listroles()
    print("{:<4} {:<15}".format(
        'Id', 'Name'))
    for role in roles:
        print("{id:<4} {name:<15}".format(**role))



# override the default 127.0.0.1 binding address
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("createdb", CreateDb)

if __name__ == "__main__":
    manager.run()
