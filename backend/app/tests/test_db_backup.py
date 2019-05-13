from unittest import TestCase, skip
import os
import json
import ddt

from app.tests import TestUtils, TEST_ASSET_ROOT
import app
from app import components


class MyAttr(dict):
    pass


def load(filename):
    with open(os.path.join(TEST_ASSET_ROOT, filename)) as f:
        res = MyAttr()
        res.update(json.load(f))
        setattr(res, "__name__", filename.replace(".", "_"))
        return res


def verify(filename):
    pass


@ddt.ddt
class TestBackupRestore(TestUtils, TestCase):

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    @ddt.data(
        verify("db_1.json")
    )
    @skip("Not implemented")
    def test_backup(self, file):
        pass

    @ddt.data(
        load("db_1.json")
    )
    @skip("Not implemented")
    def test_restore(self, data):
        components._database_restore(app.MODELS, data)
        pass
