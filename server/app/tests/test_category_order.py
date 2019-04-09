from unittest import TestCase, skip
import json

from app import components
from app.tests import TestUtils


class TestCategoryMerge(TestUtils, TestCase):

    CATEGORY_LIST = components.BASE_PATH + "/categories/"
    CATEGORY_GET = components.BASE_PATH + "/categories/{id}/"

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        self._db.close()

    def _insert_category(self, payload, mock_user=TestUtils.REGULAR_USER):
        return self.response(self.app.post(
            self.CATEGORY_LIST,
            data=json.dumps(payload),
            **self.post_args,
            **self.create_user_header(mock_user)
        ), status=201)

    def _insert_categories(self):
        categories = []

        root_category = {
            "name": "Root Category",
            "parent": None
        }
        root_category_json = self._insert_category(root_category)
        root_id = root_category_json["id"]
        categories.append(root_category)

        child_categories = [{
            "name": "Child Category " + str(i),
            "parent": {"id": root_id}
        } for i in range(3)]

        categories.extend([self._insert_category(payload) for payload in child_categories])
        return categories
