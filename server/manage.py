# coding=utf-8
import logging
import os
import sys

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from app import app
from flask_script import Server, Manager, Command, Option

manager = Manager(app)

class RunTests(Command):
    def run(self):
        import unittest
        unittest.main()

# override the default 127.0.0.1 binding ddress
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("test", RunTests)

if __name__ == "__main__":
    manager.run()
