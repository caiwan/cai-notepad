from unittest import TestCase
import json

from app import components
from app.tests import TestUtils


API_BASE = components.BASE_PATH


class TestCategoryCrud(TestUtils, TestCase):

    CATEGORY_LIST = API_BASE + "/categories/"
    CATEGORY_GET = API_BASE + "/categories/{id}/"

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        self._db.close()

    # curd
    def test_update(self):
        pass

    def test_delete(self):
        pass

    # Permissions
    def test_update_rights(self):
        pass

    def test_delete_rights(self):
        pass

    # Parents

    def test_add_category_wo_parent(self):
        # given
        # - category structure without parent
        category = {
            "name": "Category",
            "parent": None
        }

        # when
        # - insert
        insert_category_json = self._insert_category(category)
        insert_category_id = insert_category_json["id"]

        # then
        # - the newly created category should be read back
        response = self.app.get(
            self.CATEGORY_GET.format(id=insert_category_id),
            **self.post_args,
            **self.create_user_header(mock_user=TestUtils.REGULAR_USER)
        )

        self.assertEquals(200, response.status_code)
        category_json = json.loads(response.data)

        self.assertIsNotNone(category_json["id"])
        self.assertIsNone(category_json["parent"])
        self.assertEqual(category["name"], category_json["name"])

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
        response = self.app.get(
            API_BASE + "/categories/" + str(root_id) + "/",
            **self.post_args
        )
        self.assertEquals(200, response.status_code)
        root_category_json = json.loads(response.data)

        response = self.app.get(
            self.CATEGORY_GET.format(id=insert_category_id),
            **self.post_args,
            **self.create_user_header(mock_user=TestUtils.REGULAR_USER)
        )

        self.assertEquals(200, response.status_code)
        category_json = json.loads(response.data)

        self.assertIsNotNone(category_json["id"])
        self.assertIsNone(category_json["parent"])
        self.assertEqual(category["name"], category_json["name"])


    def _insert_category(self, payload, mock_user=TestUtils.REGULAR_USER):
        response = self.app.post(
            self.CATEGORY_LIST,
            data=json.dumps(payload),
            **self.post_args,
            **self.create_user_header(mock_user)
        )
        self.assertEquals(201, response.status_code)
        category_json = json.loads(response.data)
        self.assertIsNotNone(category_json["id"])
        return category_json
