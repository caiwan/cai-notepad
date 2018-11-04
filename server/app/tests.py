# coding=utf-8
import logging
import os, sys
import tempfile
import unittest

# fix import paths for internal imports
cmd_folder = os.path.dirname(__file__)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

if __name__ == '__main__':
    unittest.main()
