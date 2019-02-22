# coding=utf-8
from unittest import TestCase, skip
import json

from app import components
from app.tests import TestUtils


class TestAdmin(TestUtils, TestCase):

    USER_LIST = components.BASE_PATH + "/users/"
    USER_GET = components.BASE_PATH + "/users/{id}/"

    user = {
        "name": "testuser",
        "password": "testpassword",
        "display_name": "Test User"
    }

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        self._db.close()

    def test_create(self):
        # given
        # - data in fixture
        # when
        # - insert a new user
        user_json = self.response(self.app.post(
            self.USER_LIST,
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER))
        )

        # then
        # - new user is added
        self.assertTrue("id" in user_json)
        self.assertTrue("user_id" in user_json)
        pass

    @skip("Not implemented")
    def test_read(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_update(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_delete(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_list(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_create_rights(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_read_rights(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_update_rights(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_delete_rights(self):
        # given
        # when
        # then
        pass

    @skip("Not implemented")
    def test_list_rights(self):
        # given
        # when
        # then
        pass
