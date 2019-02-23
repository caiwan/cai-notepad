#!/usr/bin/env
# coding=utf-8
import logging
from flask_script import Server, Manager, Command
from dotenv import load_dotenv, find_dotenv
import os
import sys

import app


# fix import paths for internal imports
cmd_folder = os.path.dirname(os.path.abspath(__file__))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

load_dotenv(find_dotenv())

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


def userService():
    # terrible, terrible hack
    logging.getLogger().setLevel(logging.ERROR)
    from app.user import userService
    return userService


@manager.command
def runtests():
    """Runs all the unit and integration tests"""
    # import tests
    # tests.runAll()
    pass


@manager.command
def adduser(username, password):
    """Adds a new user"""

    pass


@manager.command
def rmuser(username):
    """Removes an existing user"""
    pass


@manager.command
@manager.option("-p", "--password", dest="password", default=None)
@manager.option("-a", "--active", dest="is_active", default=None)
def setuser(username, *args, **kwargs):
    """Sets a user's credentials and other parameters"""
    pass


@manager.command
def assignrole(username, role):
    """Adds a role to an user"""
    pass


@manager.command
def revokerole(username, role):
    """Revokes a role from a user"""
    pass


@manager.command
def listusers():
    """Lists all the existing users"""
    pass


@manager.command
def listroles():
    """Lists all the existing roles"""
    pass


# override the default 127.0.0.1 binding address
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("createdb", CreateDb)

if __name__ == "__main__":
    manager.run()
