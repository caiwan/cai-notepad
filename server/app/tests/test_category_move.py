from unittest import TestCase, skip
import json

from app import components
from app.tests import TestUtils


class TestCategoryMove(TestUtils, TestCase):

    CATEGORY_LIST = components.BASE_PATH + "/categories/"
    CATEGORY_GET = components.BASE_PATH + "/categories/{id}/"

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()
        self.categories = self._insert_categories()

    def tearDown(self):
        self._db.close()

    # --- TEST CASES

    # - move within the same parent - before first element
    def test_move_before_first(self):
        # given
        # - a category with parent
        category = self.categories[3]
        # when
        # - order is changed
        category["order"] = 0
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))
        # then
        # - the element should be the first element among children
        self.assertEquals(0, category_json["order"])

        # - this shopuld already be in order too, due it's inorder iterated and ordered by global_order
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(5, len(category_tree))
        self.assertEqual(category["id"], category_tree[0]["id"])

    # - move within the same parent - after last element
    def test_move_after_last(self):
        # given
        # - a category with parent
        category = self.categories[3]
        # when
        # - order is changed
        category["order"] = 5
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))
        # then
        # - the element should be the last element among children
        self.assertEquals(4, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(5, len(category_tree))
        self.assertEqual(category["id"], category_tree[4]["id"])

    # - move within the same parent - within first and last
    @skip("Not implemented")
    def test_move_inbetween(self):
        # given
        # - a category with parent
        category = self.categories[3]
        # when
        # - order is changed
        category["order"] = category["order"] - 1
        self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))
        # then
        # - the order should be changed accordingly

    # - move to another parent
    # - note that access rights are already tested here

    @skip("Not implemented")
    def test_move_to_root(self):
        pass

    # --- UTILS
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
            "parent": root_id
        } for i in range(5)]

        categories.extend([self._insert_category(payload)
                           for payload in child_categories])
        return categories

    def _insert_category(self, payload, mock_user=TestUtils.REGULAR_USER):
        return self.response(self.app.post(
            self.CATEGORY_LIST,
            data=json.dumps(payload),
            **self.post_args,
            **self.create_user_header(mock_user)
        ), status=201)

    def _get_categories(self, parent_id, mock_user=TestUtils.REGULAR_USER):
        categories = []
        for category in self.response(self.app.get(self.CATEGORY_LIST, **self.create_user_header(mock_user))):
            if category["parent"] == parent_id:
                categories.append(category)
        return categories
