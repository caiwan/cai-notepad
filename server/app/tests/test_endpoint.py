# coding=utf-8

from unittest import TestCase
import json
import ddt

from app import components
from app.tests import TestUtils

API_BASE = components.BASE_PATH


class MyAttr(dict):
    pass


def attr(path, method, payload=None, params=None, as_user=None, expected_status=[200, 201]):
    r = MyAttr({"path": path, "method": method, "payload": payload, "params": params, "as_user": as_user, "expected_status": expected_status})
    setattr(r, "__name__", "%s_%s_as_%s" % (method, path.replace("/", "_"), as_user if as_user else "anonymous"))
    return r


@ddt.ddt
class TestEndpointAccess(TestUtils, TestCase):

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()
        pass

    @ddt.data(
        # auth
        attr("/auth/register/", "post", payload={}),
        attr("/auth/login/", "post", payload={}),
        attr("/auth/logout/", "post", as_user="user"),
        attr("/auth/renew/", "post", as_user="user", payload={}),
        attr("/auth/password_reset/", "post", as_user="user", payload={}),
        attr("/auth/profile/", "post", as_user="user"),
        attr("/auth/profile/", "put", as_user="user", payload={}),

        # user
        attr("/users/", "get", as_user="admin"),
        attr("/users/", "post", as_user="admin", payload={}),
        attr("/users/1/", "get", as_user="admin"),
        attr("/users/1/", "put", as_user="admin", payload={}),
        attr("/users/1/", "delete", as_user="admin"),

        # notes
        attr("/notes/", "get", as_user="user"),
        attr("/notes/", "post", as_user="user", payload={}),
        attr("/notes/1/", "get", as_user="user"),
        attr("/notes/1/", "put", as_user="user", payload={}),
        attr("/notes/1/", "delete", as_user="user"),

        # tasks
        attr("/tasks/", "get", as_user="user"),
        attr("/tasks/", "post", as_user="user", payload={}),
        attr("/tasks/1/", "get", as_user="user"),
        attr("/tasks/1/", "put", as_user="user", payload={}),
        attr("/tasks/1/", "delete", as_user="user"),

        # categories
        attr("/categories/", "get", as_user="user"),
        attr("/categories/", "post", as_user="user", payload={}),
        attr("/categories/1/", "get", as_user="user"),
        attr("/categories/1/", "put", as_user="user", payload={}),
        attr("/categories/1/", "delete", as_user="user"),

        # tag autosearch
        attr("/tags/autocomplete/", "get", params={"q": ""}, as_user="user")

    )
    def test_endpoint(self, attr):

        methods = {
            "get": self.app.get,
            "post": self.app.post,
            "put": self.app.put,
            "patch": self.app.patch,
            "delete": self.app.delete,
        }

        if attr["method"] not in methods:
            self.fail()

        method = methods[attr["method"]]
        args = dict(**self.post_args)
        if attr["payload"]:
            args["data"] = json.dumps(attr["payload"])

        if attr["params"]:
            args["query_string"] = attr["params"]

        if attr["as_user"]:
            if "headers" not in args:
                args["headers"] = {}
            args["headers"]["Authentication"] = self.create_user_token(attr["as_user"])

        response = method(API_BASE + attr["path"], **args)

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        self.assertTrue(response.status_code in attr["expected_status"], msg="Status code: %d Response: %s" % (response.status_code, response.data))
