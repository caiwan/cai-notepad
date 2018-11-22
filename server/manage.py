# coding=utf-8
import logging
import os
import sys

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except: 
    logging.info("No dotenv, using envvars")
    pass

import app 
from flask_script import Server, Manager, Command, Option

manager = Manager(app.app)

class CreateDb(Command):
    def run(self):
        from app import components
        components.create_tables(app.app, app.models) 

class RunTests(Command):
    def run(self):
        import unittest
        unittest.main()

# override the default 127.0.0.1 binding ddress
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("test", RunTests)
manager.add_command("createdb", CreateDb)

if __name__ == "__main__":
    manager.run()
