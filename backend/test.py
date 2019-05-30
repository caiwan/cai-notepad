# coding=utf-8
from dotenv import load_dotenv
# from dotenv import find_dotenv
import os
import sys
import unittest

from tests import test_runner


# load_dotenv(find_dotenv())
load_dotenv("test.env")


# add import paths for internal imports
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


if __name__ == "__main__":
    all = unittest.TestLoader().discover(cmd_folder + "/app/tests")
    runner = test_runner.TestRunner()
    runner.run(all)
