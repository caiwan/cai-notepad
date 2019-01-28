# coding=utf-8
from dotenv import load_dotenv
import os, sys
import unittest

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

load_dotenv("dev.env")


if __name__ == "__main__":
    all = unittest.TestLoader().discover(cmd_folder)
    unittest.TextTestRunner(verbosity=2).run(all)
