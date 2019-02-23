# coding=utf-8
from dotenv import load_dotenv, find_dotenv
import os
import sys
import unittest


load_dotenv(find_dotenv())

# fix import paths for internal imports
cmd_folder = os.path.dirname(os.path.abspath(__file__))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


def runAll():
    all = unittest.TestLoader().discover(cmd_folder + "/app")
    unittest.TextTestRunner(verbosity=2).run(all)


if __name__ == "__main__":
    runAll()
