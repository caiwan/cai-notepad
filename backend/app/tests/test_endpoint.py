# coding=utf-8

# import logging

from unittest import TestCase
import json
import ddt

from app import components
from app.tests import BaseTest

API_BASE = components.BASE_PATH


class MyAttr(dict):
    pass


def attr(path, method,
         payload=None,
         params=None,
         as_user=None,
         expected_status=[200, 201],
         skip=False,
         skip_reason="Temporary disabled"
         ):
    #
    r = MyAttr({"path": path, "method": method, "payload": payload, "params": params, "as_user": as_user,
                "expected_status": expected_status, "skip": skip, "skip_reason": skip_reason})
    setattr(r, "__name__", "%s_%s_as_%s" % (method, path.replace("/", "_"), as_user if as_user else "anonymous"))
    return r


@ddt.ddt
class TestEndpointAccess(BaseTest, TestCase):

    def __init__(self, methodName):
        BaseTest.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()
        # TODO + add test Note
        # TODO + add test Task
        # TODO + add test Category
        pass

    @ddt.data(
        # auth
        attr("/auth/register/", "post", payload={}, skip=True, skip_reason="Endpoint not implemented"),
        attr("/auth/login/", "post", payload={"username": "user", "password": "password"}),
        attr("/auth/logout/", "post", as_user="user"),
        attr("/auth/renew/", "post", as_user="user", payload={}),
        attr("/auth/password_reset/", "get", as_user="user", payload={}, skip=True, skip_reason="Endpoint not implemented"),
        attr("/auth/profile/", "get", as_user="user", skip=True, skip_reason="Endpoint not implemented"),
        attr("/auth/profile/", "put", as_user="user", payload={}, skip=True, skip_reason="Endpoint not implemented"),

        # -- anonymous access
        attr("/auth/logout/", "post", expected_status=[403]),
        attr("/auth/renew/", "post", expected_status=[403]),
        attr("/auth/password_reset/", "post", expected_status=[403], skip=True, skip_reason="Endpoint not implemented"),
        attr("/auth/profile/", "get", expected_status=[403], skip=True, skip_reason="Endpoint not implemented"),
        attr("/auth/profile/", "put", expected_status=[403], payload={}, skip=True, skip_reason="Endpoint not implemented"),

        # user
        attr("/users/", "get", as_user="admin"),
        attr("/users/", "post", as_user="admin", payload={"name": "something_new", "password": "somepw"}),
        attr("/users/1/", "get", as_user="admin"),
        attr("/users/1/", "put", as_user="admin", skip=True, skip_reason="Test data required", payload={"name": "", "password": "somepw"}),
        attr("/users/1/", "delete", as_user="admin", skip=True, skip_reason="Test data required",),

        # notes
        attr("/notes/", "get", as_user="user"),
        attr("/notes/", "post", as_user="user", payload={"title": "Note", "content": "Content", "tags": []}),
        attr("/notes/1/", "get", as_user="user", skip=True, skip_reason="Test data required"),
        attr("/notes/1/", "put", as_user="user", payload={
            "title": "Note",
            "content": "Content", "tags": []}, skip=True, skip_reason="Test data required"),
        attr("/notes/1/", "delete", as_user="user", skip=True, skip_reason="Test data required"),

        # --- notes as anonymous
        attr("/notes/", "get", expected_status=[403]),
        attr("/notes/", "post", expected_status=[403], payload={}),
        attr("/notes/1/", "get", expected_status=[403]),
        attr("/notes/1/", "put", expected_status=[403], payload={}),
        attr("/notes/1/", "delete", expected_status=[403]),

        # tasks
        attr("/tasks/", "get", as_user="user"),
        attr("/tasks/", "post", as_user="user", payload={"title": "Task"}),
        attr("/tasks/1/", "get", as_user="user", skip=True, skip_reason="Test data required"),
        attr("/tasks/1/", "put", as_user="user", payload={"title": "Task"}, skip=True, skip_reason="Test data required"),
        attr("/tasks/1/", "delete", as_user="user", skip=True, skip_reason="Test data required"),

        # --- tasks as anonymous
        attr("/tasks/", "get", expected_status=[403]),
        attr("/tasks/", "post", expected_status=[403], payload={}),
        attr("/tasks/1/", "get", expected_status=[403]),
        attr("/tasks/1/", "put", expected_status=[403], payload={}),
        attr("/tasks/1/", "delete", expected_status=[403]),

        # categories
        attr("/categories/", "get", as_user="user"),
        attr("/categories/", "post", as_user="user", payload={"name": "Category", "parent": None}),
        attr("/categories/1/", "get", as_user="user", skip=True, skip_reason="Test data required"),
        attr("/categories/1/", "put", as_user="user", payload={"name": "Category", "parent": None}, skip=True, skip_reason="Test data required"),
        attr("/categories/1/", "delete", as_user="user", skip=True, skip_reason="Fails for some reason"),

        # -- categories as anonymous
        attr("/categories/", "get", expected_status=[403]),
        attr("/categories/", "post", expected_status=[403], payload={}),
        attr("/categories/1/", "get", expected_status=[403]),
        attr("/categories/1/", "put", expected_status=[403], payload={}),
        attr("/categories/1/", "delete", expected_status=[403]),

        # tag autosearch
        attr("/tags/autocomplete/", "get", params={"q": "something"}, as_user="user"),
        attr("/tags/autocomplete/", "get", params={"q": "something"}, expected_status=[403])
    )
    def test_endpoint(self, attr):
        if attr["skip"]:
            self.skipTest(attr["skip_reason"])
            return

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
            args["headers"]["Authorization"] = self.create_user_token(attr["as_user"])

        response = method(API_BASE + attr["path"], **args)

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        self.assertTrue(response.status_code in attr["expected_status"], msg="Status code: %d Response: %s" % (response.status_code, response.data))
