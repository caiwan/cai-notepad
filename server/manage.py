# coding=utf-8
import logging
import os
import sys

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from app.main import app
from flask_script import Server, Manager, Command, Option


class InitDb(Command):
    option_list = (
        Option('--user', '-u', dest='user_name'),
        Option('--pass', '-p', dest='password'),
        Option('--db', '-d', dest='admin_db'),
        Option('--host', '-h', dest='host')
    )

    def run(self, user_name, password, admin_db, host):
        from mongoengine import connect
        connect(admin_db, username=user_name, password=password, host=host)
        print("OK")
        # There's no way to add users this way to the db :(
        pass
    pass


manager = Manager(app)

# override the default 127.0.0.1 binding ddress
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("initdb", InitDb)

if __name__ == "__main__":
    manager.run()
