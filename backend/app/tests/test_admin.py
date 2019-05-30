# coding=utf-8
from unittest import TestCase, skip
import json

from app import components
from app.tests import BaseTest


class TestAdmin(BaseTest, TestCase):

    USER_LIST = components.BASE_PATH + "/users/"
    USER_GET = components.BASE_PATH + "/users/{id}/"

    user = {
        "name": "testuser",
        "password": "testpassword",
        "display_name": "Test User"
    }

    def __init__(self, methodName):
        BaseTest.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        # self._db.close()
        pass

    def test_create(self):
        # given
        # - data in fixture
        # when
        # - insert a new user
        user_json = self.response(self.app.post(
            self.USER_LIST,
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER)), status=201
        )

        # then
        # - new user is added
        self.assertTrue("id" in user_json)
        self.assertTrue("user_ref_id" in user_json)

    def test_create_rights(self):
        # given
        # when
        response = self.response(self.app.post(
            self.USER_LIST,
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.REGULAR_USER)), status=403
        )

        # then
        self.assertTrue("message" in response)

    def test_read(self):
        # given
        user_json = self.response(self.app.post(
            self.USER_LIST,
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER)), status=201
        )
        # when
        user_get_json = self.response(self.app.get(
            self.USER_GET.format(id=user_json["id"]),
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER))
        )
        # then
        self.assertTrue("id" in user_get_json)
        self.assertTrue("user_ref_id" in user_get_json)

    def test_read_rights(self):
        # given
        user_json = self.response(self.app.post(
            self.USER_LIST,
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER)), status=201
        )
        # when
        response = self.response(self.app.get(
            self.USER_GET.format(id=user_json["id"]),
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.REGULAR_USER)), status=403
        )
        # then
        self.assertTrue("message" in response)

    @skip("Not implemented")
    def test_update(self):
        # XXX given
        # XXX when
        # XXX then
        pass

    @skip("Not implemented")
    def test_update_rights(self):
        # XXX given
        # XXX when
        # XXX then
        pass

    def test_delete(self):
        # given
        user_json = self.response(self.app.post(
            self.USER_LIST,
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER)), status=201
        )
        # when
        response = self.response(self.app.delete(
            self.USER_GET.format(id=user_json["id"]),
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER))
        )
        self.assertEqual(0, len(response))
        # then

        response = self.response(self.app.get(
            self.USER_GET.format(id=user_json["id"]),
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER)), status=404
        )
        self.assertTrue("message" in response)

    def test_delete_rights(self):
        # given
        user_json = self.response(self.app.post(
            self.USER_LIST,
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.ADMIN_USER)), status=201
        )

        # when
        response = self.response(self.app.delete(
            self.USER_GET.format(id=user_json["id"]),
            data=json.dumps(self.user),
            ** self.post_args,
            **self.create_user_header(self.REGULAR_USER)), status=403
        )
        # then
        self.assertTrue("message" in response)

    @skip("Not implemented")
    def test_list(self):
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
