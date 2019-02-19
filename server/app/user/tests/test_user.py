# coding=utf-8
from unittest import TestCase, skip
import json

from app import components
from app.tests import TestUtils

from app.user.model import Token

API_BASE = components.BASE_PATH


class TestUser(TestUtils, TestCase):

    LOGIN = API_BASE + "/auth/login/"
    LOGOUT = API_BASE + "/auth/logout/"

    PROFILE = API_BASE + "/auth/profile/"

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        self._db.close()

    skip("Registration is not implemented yet")
    def test_register(self):
        # given no user
        # when register a new user
        # then registration shall be succeed
        self.fail("Registration is not implemented yet")
        pass

    def test_login(self):
        # given user
        credentials = {
            "username": self.REGULAR_USER,
            "password": self.REGULAR_PW
        }

        # when login
        response = self.app.post(self.LOGIN, data=json.dumps(credentials), **self.post_args)
        response_json = self.response(response)

        # then a valid login token shall be given
        self.assertTrue("token" in response_json, msg="no token was given")
        token_id = response_json["token"]

        try:
            token = Token.get(Token.token_id == token_id)
            self.assertEqual(self.REGULAR_USER, token.user.name)
        except Token.DoesNotExist:
            self.fail("No valid token was saved")

        pass

    @skip("Token security check is not implemented yet")
    def test_token(self):
        # TODO
        # given user with login and token
        # when requesting a protected resource
        # then a resource should be accessed without error
        self.fail("Token security check is not implemented yet")

        pass

    @skip("Permission security is not implemented yet")
    def test_permissions(self):
        # TODO
        self.fail("Permission security is not implemented yet")
        pass

    def test_logout(self):
        # given
        # - user with login and token
        credentials = {
            "username": self.REGULAR_USER,
            "password": self.REGULAR_PW
        }
        response = self.app.post(self.LOGIN, data=json.dumps(credentials), **self.post_args)
        response_json = self.response(response)
        self.assertTrue("token" in response_json, msg="no token was given")
        token_id = response_json["token"]

        # when
        # - logout
        response = self.app.get(self.LOGOUT, **self.post_args, headers={
            "Authorization": "Bearer %s" % token_id
        })

        # then
        # - an access token shall be removed
        try:
            token = Token.get(Token.token_id == token_id)
            self.fail("No token ws deleted, still active %s" % token.token_id)
        except Token.DoesNotExist:
            pass
