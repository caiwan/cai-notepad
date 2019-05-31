from unittest import TestCase, skip
import json

from app import components
from app.tests import BaseTest


class TestCategoryMove(BaseTest, TestCase):

    CATEGORY_LIST = components.BASE_PATH + "/categories/"
    CATEGORY_GET = components.BASE_PATH + "/categories/{id}/"

    def __init__(self, methodName):
        BaseTest.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()
        self.categories = self._insert_categories()

    def tearDown(self):
        pass

    # --- TEST CASES

    # - move within the same parent - before first element
    def test_move_before_first(self):
        # given
        # - a category: the 3rd child (0.2) of the root element
        category = self.categories[3]
        # when
        # - order is changed: move to position 0
        category["order"] = 0
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - the element should be the first element among children at index 0 position 0.0
        self.assertEquals(0, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(5, len(category_tree))
        self.assertEqual(category["id"], category_tree[0]["id"])

    # - move within the same parent - after last element
    def test_move_after_last(self):
        # given
        # - a category: the 3rd child (0.2) of the root element
        category = self.categories[3]
        # when
        # - order is changed: move to position 5
        category["order"] = 5
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - the element should be the last element among children at index 4 position 0.4
        self.assertEquals(4, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(5, len(category_tree))
        self.assertEqual(category["id"], category_tree[4]["id"])

    # - move within the same parent - within first and last
    def test_move_in_between(self):
        # given
        # - a category: the 3rd child (0.2) of the root element
        category = self.categories[3]
        # when
        # - order is changed: move to position 1 (0.1)
        category["order"] = 1  # category["order"] - 1
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - the order should be changed accordingly: at index 1 position 0.1
        self.assertEquals(1, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(5, len(category_tree))
        self.assertEqual(category["id"], category_tree[1]["id"])

    def test_move_to_root_at_first(self):
        # given
        # - a category: the 3rd child of the 2nd root element
        category = self.categories[9]
        # when
        # - move before the first root element at position 0
        category["order"] = 0
        category["parent"] = None
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - a category should be moved accordingly at index 0 position 0
        self.assertEquals(0, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(4, len(category_tree))
        self.assertEqual(category["id"], category_tree[0]["id"])
        pass

    def test_move_to_root_at_last(self):
        # given
        # - a category: the 3rd child of the 2nd root element at position 1.2
        category = self.categories[9]
        # when
        # - move after the last root element at position 3
        category["order"] = 3
        category["parent"] = None
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - a category should be moved accordingly at index 3 position 3
        self.assertEquals(3, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(4, len(category_tree))
        self.assertEqual(category["id"], category_tree[3]["id"])
        pass

    def test_move_to_root_in_between(self):
        # given
        # - a category: the 3rd child of the 2nd root element at position 1.2
        category = self.categories[9]
        # when
        # - move after the 2nd root element at position 2
        category["order"] = 2
        category["parent"] = None
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - a category should be moved accordingly at index 2 position 2
        self.assertEquals(2, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        self.assertEqual(4, len(category_tree))
        self.assertEqual(category["id"], category_tree[2]["id"])
        pass

    def test_move_child_to_another_root(self):
        # given
        # - a category: the 3rd child of the 2nd root element
        category = self.categories[9]
        # when
        # - move to after the 2nd child ot the 1s root element
        category["order"] = 2
        category["parent"] = self.categories[0]["id"]
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        self.assertEquals(2, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        # - the root category should have 6 children
        self.assertEqual(6, len(category_tree))
        # - a category should be moved accordingly at index 2 position 0.2
        self.assertEqual(category["id"], category_tree[2]["id"])
        # - the old category the 2nd should have 4 children
        category_tree = self._get_categories(self.categories[6]["id"])
        self.assertEqual(4, len(category_tree))
        pass

    def test_move_root_to_child_of_another(self):
        # given
        # - the 1st root category
        category = self.categories[0]
        # when
        # - move after the 2nd child ot the 2nd root element
        category["order"] = 2
        category["parent"] = self.categories[6]["id"]
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category["id"]),
            data=json.dumps(category),
            **self.post_args,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        self.assertEquals(2, category_json["order"])
        category_tree = self._get_categories(category_json["parent"])
        # - the 2nd root category should have 6 children
        self.assertEqual(6, len(category_tree))
        # - a category should be moved accordingly at index 2 position 1.2
        self.assertEqual(category["id"], category_tree[2]["id"])
        # - the root should have 2 children
        category_tree = self._get_categories(None)
        self.assertEqual(2, len(category_tree))
        pass
        pass

    # --- UTILS
    def _insert_categories(self):
        # Will create all the stuff
        # id: comment path
        # 0: --- 1st Root element 0
        # 1: 1st child 0.0
        # 2: 2nd child 0.1
        # 3: 3rd child 0.2
        # 4: 4th child 0.3
        # 5: 5th child 0.4
        # 6: --- 2nd Root element 1
        # 7: 1st child 1.0
        # 8: 2nd child 1.1
        # 9: 3rd child 1.2
        # 10: 4th child 1.3
        # 11: 5th child 1.4
        # 12: -- 3rd Root element 2
        # 13: 1st child 2.0
        # 14: 2nd child 2.1
        # 15: 3rd child 2.2
        # 16: 4th child 2.3
        # 17: 5th child 2.4

        categories = []

        for root_category in [{
            "name": "Root Category %d" % (i),
            "parent": None
        } for i in range(3)]:
            root_category_json = self._insert_category(root_category)
            root_id = root_category_json["id"]
            categories.append(root_category_json)

            categories.extend([self._insert_category(payload) for payload in [{
                "name": "Child Category %d of %s" % (j, root_category["name"]),
                "parent": root_id
            } for j in range(5)]])
        return categories

    def _insert_category(self, payload, mock_user=BaseTest.REGULAR_USER):
        return self.response(self.app.post(
            self.CATEGORY_LIST,
            data=json.dumps(payload),
            **self.post_args,
            **self.create_user_header(mock_user)
        ), status=201)

    def _get_categories(self, parent_id, mock_user=BaseTest.REGULAR_USER):
        categories = []
        for category in self.response(self.app.get(self.CATEGORY_LIST, **self.create_user_header(mock_user))):
            if category["parent"] == parent_id:
                categories.append(category)
        return categories
