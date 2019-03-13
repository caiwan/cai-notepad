from unittest import TestCase, skip
import json

from app import components
from app.tests import TestUtils


class TestCategoryCrud(TestUtils, TestCase):

    CATEGORY_LIST = components.BASE_PATH + "/categories/"
    CATEGORY_GET = components.BASE_PATH + "/categories/{id}/"

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        self._db.close()

    # curd
    def test_update(self):
        # Given
        # - one category
        category = {
            "name": "Category",
            "parent": None
        }
        category_json = self._insert_category(category)
        self._validate_fields(category_json)
        category_id = category_json["id"]

        # When
        # - update it with new data
        updated_category = {
            "name": "Updated Category",
            "parent": None
        }
        category_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category_id),
            data=json.dumps(updated_category),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        # Then
        # - Details should be updated
        self._validate_fields(category_json)
        self.assertEqual(category_id, category_json["id"])
        self.assertEqual(updated_category["name"], category_json["name"])
        pass

    @skip("Not implemented")
    def test_delete(self):
        # TODO: Delete -> Something like a merge of categories
        pass

    # Permissions
    def test_update_rights(self):
        # Given
        # - one category created by an user
        category = {
            "name": "Category",
            "parent": None
        }
        category_json = self._insert_category(category)
        self._validate_fields(category_json)
        category_id = category_json["id"]

        # When
        # - attempt update it with another user
        updated_category = {
            "name": "Updated Category",
            "parent": None
        }
        error_json = self.response(self.app.put(
            self.CATEGORY_GET.format(id=category_id),
            data=json.dumps(updated_category),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER)
        ), status=404)

        # Then
        # - Error should be given
        self.assertTrue("message" in error_json)

    @skip("Not implemented")
    def test_delete_rights(self):
        # TODO: Delete -> Something like a merge of categories
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
        category_json = self.response(self.app.get(
            self.CATEGORY_GET.format(id=insert_category_id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        self._validate_fields(category_json)

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
        child_categories = [self._insert_category(payload) for payload in child_categories]
        child_categories_id = [item["id"] for item in child_categories]

        # then
        # - check parent-child relationship
        root_category_json = self.response(self.app.get(
            self.CATEGORY_GET.format(id=root_id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        responses = [self.response(self.app.get(
            self.CATEGORY_GET.format(id=id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        )) for id in child_categories_id]

        for (category, category_json) in zip(child_categories, responses):

            self._validate_fields(category_json)

            self.assertEqual(category["id"], category_json["id"])
            self.assertIsNotNone(category_json["parent"])
            self.assertEqual(root_category_json["id"], category_json["parent"])
            self.assertEqual(category["name"], category_json["name"])

    @skip("Not implemented")
    def test_add_category_w_nonexistent_parent():
        pass

    @skip("Not implemented")
    def test_add_category_w_parent_rights():
        pass

    # Test ordering / reordering

    # TODO: ...

    def _insert_category(self, payload, mock_user=TestUtils.REGULAR_USER):
        category_json = self.response(self.app.post(
            self.CATEGORY_LIST,
            data=json.dumps(payload),
            **self.post_args,
            **self.create_user_header(mock_user)
        ), status=201)
        return category_json

    def _validate_fields(self, category_json):
        self.assertTrue("flatten_order" not in category_json)
        self.assertTrue("id" in category_json)
        self.assertIsNotNone(category_json["id"])
