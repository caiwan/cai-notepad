# coding=utf-8
import logging

from app.main import app
from flask_script import Server, Manager, Command

# https://flask-script.readthedocs.io/en/latest/
manager = Manager(app)

# override the default 127.0.0.1 binding ddress
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))

if __name__ == "__main__":
    manager.run()
