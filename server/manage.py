# coding=utf-8
from flask_script import Server, Manager, Command
from dotenv import load_dotenv, find_dotenv
import os
import sys

import app

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
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


class RunTests(Command):
    def run(self):
        import unittest
        unittest.main()


# override the default 127.0.0.1 binding ddress
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))
manager.add_command("test", RunTests)
manager.add_command("createdb", CreateDb)

if __name__ == "__main__":
    manager.run()
