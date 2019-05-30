from unittest import TestCase
import json

from app.tests import BaseTest
from app import components


class TestNoteFiltering(TestCase, BaseTest):

    CATEGORY_LIST = components.BASE_PATH + "/categories/"
    CATEGORY_GET = components.BASE_PATH + "/categories/{id}/"

    NOTE_LIST = components.BASE_PATH + "/notes/"
    NOTE_GET = components.BASE_PATH + "/notes/{id}/"

    def __init__(self, methodName):
        TestCase.__init__(self, methodName)
        BaseTest.__init__(self)

    def setUp(self):
        self._setup_app()
        self.categories = self._create_categories()
        self.notes = self._create_notes(self.categories)

    def tearDown(self):
        self._db.close()

    def test_select_category_all(self):
        # given
        # - all 4 + 1 categories, 15 notes total
        # when
        # - select 'all'
        query_string = {"category": "all"}
        response_json = self.response(self.app.get(
            self.NOTE_LIST,
            **self.post_args, query_string=query_string,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))

        # then
        # - should receive all the 15 notes
        self.assertEqual(15, len(response_json))

        pass

    def test_select_category_unassigned(self):
        # given
        # - 3 notes total without category (None)
        # when
        # - select 'unassigned'
        query_string = {"category": "unassigned"}
        response_json = self.response(self.app.get(
            self.NOTE_LIST,
            **self.post_args, query_string=query_string,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - should receive all the 3 notes unassigned
        self.assertEqual(3, len(response_json))
        for note in response_json:
            self.assertEqual(None, note["category"])
        pass

    def test_select_one_category(self):
        # given
        # - one category without children [3], notes assigned to it
        categoryId = self.categories[3]["id"]
        # when
        # - select that category
        query_string = {"category": categoryId}
        response_json = self.response(self.app.get(
            self.NOTE_LIST,
            **self.post_args, query_string=query_string,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - should receive all the 3 notes assigned to it
        self.assertEqual(3, len(response_json))
        for note in response_json:
            self.assertEqual(categoryId, note["category"])
        pass

    def test_select_one_category_rights(self):
        # given
        # - one category children, notes assigned to it
        # - another user
        categoryId = self.categories[2]["id"]
        # when
        # - select that category from another user
        query_string = {"category": categoryId}
        error_json = self.response(self.app.get(
            self.NOTE_LIST,
            **self.post_args, query_string=query_string,
            **self.create_user_header(BaseTest.REGULAR_ALT_USER)
        ), status=404)
        # then
        # - should receive 404 and error message
        self.assertTrue("message" in error_json)

        pass

    def test_select_child_categories(self):
        # given
        # - root category [0] with children [1..3], notes assigned to it, 4 total
        categoryId = self.categories[0]["id"]
        # when
        # - select that category
        query_string = {"category": categoryId}
        response_json = self.response(self.app.get(
            self.NOTE_LIST,
            **self.post_args, query_string=query_string,
            **self.create_user_header(BaseTest.REGULAR_USER)
        ))
        # then
        # - should receive all 3 and the remaining 9 notes assigned to its children, 12 in total
        self.assertEqual(12, len(response_json))
        # TODO: how do we check this further?

        pass

    # ---- UTILS
    def _insert_note(self, note, mock_user=BaseTest.REGULAR_USER):
        note_json = self.response(self.app.post(
            self.NOTE_LIST,
            data=json.dumps(note),
            **self.post_args,
            **self.create_user_header(mock_user)
        ), status=201)
        return note_json

    def _insert_category(self, payload, mock_user=BaseTest.REGULAR_USER):
        return self.response(self.app.post(
            self.CATEGORY_LIST,
            data=json.dumps(payload),
            **self.post_args,
            **self.create_user_header(mock_user)
        ), status=201)

    def _create_categories(self):
        # will insert one root + 3 subcategories = 4 total
        categories = []

        root_category = {
            "name": "Root Category",
            "parent": None
        }
        root_category_json = self._insert_category(root_category)
        root_id = root_category_json["id"]
        categories.append(root_category_json)

        child_categories = [{
            "name": "Child Category " + str(i),
            "parent": root_id
        } for i in range(3)]

        categories.extend([self._insert_category(payload)
                           for payload in child_categories])
        return categories

    def _create_notes(self, categories):
        # will insert 3 notes to ea. cateory + 3 as unassigned
        # total 4 categories = 15 notes total
        notes = []
        for category in categories:
            notes.extend([self._insert_note({
                "title": "test_title %d" % (i),
                "content": "test_content\r\n %d \r\n" % (i),
                "tags": ["these", "are", "the", "test", "tags", "we", "look", "for"],
                "category": category["id"]}
            ) for i in range(3)])

        notes.extend([self._insert_note({
            "title": "test_title %d" % (i),
            "content": "test_content\r\n %d \r\n" % (i),
            "tags": ["these", "are", "the", "test", "tags", "we", "look", "for"],
            "category": None}
        ) for i in range(3)])
        return notes
