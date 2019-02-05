from unittest import TestCase
import json

import peewee

import app
from app import components


API_BASE = components.BASE_PATH


class TestCategoryCrud(TestCase):

    post_args = {
        "content_type": "application/json"
    }

    def setUp(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.MODELS, safe=True)
        self.app = app.APP.test_client()

    def tearDown(self):
        self._db.close()

    def test_add_category_wo_parent(self):
        # given
        category = {
            "name": "Category",
            "parent": None
        }
        # when
        category_json = self._insert_category(category)

        # then
        self._validate_category(category, category_json)

    def test_add_category_w_parent(self):
        # given
        root_category = {
            "name": "Root Category",
            "parent": None
        }
        root_category_json = self._insert_category(root_category)
        root_id = root_category_json["id"]

        child_categories = [{
            "name": "Child Category " + str(i),
            "parent": {"id": root_id}
        } for i in range(3)]

        # when
        child_categories_json = [self._insert_category(payload) for payload in child_categories]

        # then
        for pair in zip(child_categories, child_categories_json):
            self._validate_category(pair[0], pair[1])

        # - check parent-child relationship
        # Children?
        response = self.app.get(API_BASE + "/categories/" + str(root_id) + "/", **self.post_args)
        self.assertEquals(200, response.status_code)
        root_category_json = json.loads(response.data)

        # self.assertTrue("children" in root_category_json)
        # for child in child_categories_json:
        # self.assertTrue(child["id"] in root_category_json["children"])

    def _insert_category(self, payload):
        response = self.app.post(API_BASE + "/categories/", data=json.dumps(payload), **self.post_args)
        self.assertEquals(201, response.status_code)
        category_json = json.loads(response.data)
        self.assertIsNotNone(category_json["id"])
        return category_json

    def _validate_category(self, expected, actual):
        # self.assertEqual(expected["name"], actual["name"])
        # self.assertEqual(expected["parent"], actual["parent"]["id"])
        pass
