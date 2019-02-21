from unittest import TestCase
import json

from app.tests import TestUtils
from app import components


class TestNotes(TestCase, TestUtils):

    NOTE_LIST = components.BASE_PATH + "/notes/"
    NOTE_GET = components.BASE_PATH + "/notes/{id}/"

    new_note = {
        "title": "test_title",
        "content": "test_content\r\nárviz tűrő tükör fúró gép\r\n",
        "tags": ["these", "are", "the", "test", "tags", "we", "look", "for", "árviz", "tűrő", "tükör", "fúró", "gép"]
    }

    edited_note = {
        "title": "edited title",
        "content": "edited contents",
        "tags": ["these", "are", "the", "other", "tags", "we", "have", "edited", "so", "far"],
        "is_pinned": True,
        "is_archived": True
    }

    def __init__(self, methodName):
        TestCase.__init__(self, methodName)
        TestUtils.__init__(self)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        self._db.close()

    def test_create_note(self):
        # given
        # - fixture, see above

        # when
        note_json = self.response(self.app.post(
            self.NOTE_LIST,
            data=json.dumps(self.new_note),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ), status=201)

        # then
        self._validate_fields(note_json)
        self._validate_content(self.new_note, note_json)

        response_json = self.response(self.app.get(
            self.NOTE_GET.format(id=note_json["id"]),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        # TODO: Test for tags

        self._validate_fields(response_json)
        self._validate_content(note_json, response_json)

    def test_read_note(self):
        # given
        note_json = self._insert_note(self.new_note)

        self._validate_fields(note_json)
        self._validate_content(self.new_note, note_json)

        # when
        response_json = self.response(self.app.get(
            self.NOTE_GET.format(id=note_json["id"]),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        # then
        self._validate_fields(response_json)
        self._validate_content(self.new_note, response_json)

    def test_delete_note(self):
        # given
        note_json = self._insert_note(self.new_note)

        # when
        response_json = self.response(self.app.delete(
            self.NOTE_GET.format(id=note_json["id"]),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        self.assertEqual(0, len(response_json))

        # then
        response_json = self.response(self.app.get(
            self.NOTE_GET.format(id=note_json["id"]),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ), status=404)
        self.assertTrue("message" in response_json)

    def test_edit_note(self):
        # given
        # - fixture, and
        note_json = self._insert_note(self.new_note)

        # self._validate_fields(note_json)
        # self._validate_content(self.new_note, note_json)

        # when
        edited_json = self.response(self.app.put(
            self.NOTE_GET.format(id=note_json["id"]),
            data=json.dumps(self.edited_note),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        self._validate_fields(edited_json)
        self.assertEqual(note_json["id"], edited_json["id"])
        self._validate_content(self.edited_note, edited_json)

        # then
        response_json = self.response(self.app.get(
            self.NOTE_GET.format(id=note_json["id"]),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        # TODO: Test for tags

        self._validate_fields(response_json)
        self.assertEqual(note_json["id"], response_json["id"])
        self._validate_content(edited_json, response_json)

    # Permission checks

    def test_list_rights(self):
        # given
        # - notes inserted by an user

        my_notes = [self._insert_note(self.new_note, mock_user=TestUtils.REGULAR_USER) for _ in range(5)]
        alt_notes = [self._insert_note(self.new_note, mock_user=TestUtils.REGULAR_ALT_USER) for _ in range(4)]

        # when
        # - requesting notes with another user
        my_notes_read = self.response(self.app.get(
            self.NOTE_LIST,
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        ))

        alt_notes_read = self.response(self.app.get(
            self.NOTE_LIST,
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER)
        ))

        # then
        # - others notes shall not be accessable
        self.assertEquals(len(my_notes), len(my_notes_read))
        self.assertEquals(len(alt_notes), len(alt_notes_read))
        for (sent, read) in zip(my_notes + alt_notes, my_notes_read + alt_notes_read):
            self.assertTrue("owner" not in read)
            self.assertEqual(sent["title"], read["title"])

        my_ids = set([task["id"] for task in my_notes_read])
        alt_ids = set([task["id"] for task in alt_notes_read])
        self.assertFalse(bool(my_ids & alt_ids))

        pass

    def test_read_rights(self):
        # given
        note_json = self._insert_note(self.new_note)

        self._validate_fields(note_json)
        self._validate_content(self.new_note, note_json)

        # when
        response_json = self.response(self.app.get(
            self.NOTE_GET.format(id=note_json["id"]),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER)
        ), status=404)

        # then
        self.assertTrue("message" in response_json)

    def test_update_rights(self):
        # given
        note_json = self._insert_note(self.new_note)

        self._validate_fields(note_json)
        self._validate_content(self.new_note, note_json)

        # when
        response_json = self.response(self.app.put(
            self.NOTE_GET.format(id=note_json["id"]),
            data=json.dumps(self.edited_note),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER)
        ), status=404)

        # then
        self.assertTrue("message" in response_json)

    def test_delete_rights(self):
        # given
        note_json = self._insert_note(self.new_note)

        self._validate_fields(note_json)
        self._validate_content(self.new_note, note_json)

        # when
        response_json = self.response(self.app.delete(
            self.NOTE_GET.format(id=note_json["id"]),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER)
        ), status=404)

        # then
        self.assertTrue("message" in response_json)

    # utils
    def _insert_note(self, note, mock_user=TestUtils.REGULAR_USER):
        note_json = self.response(self.app.post(
            self.NOTE_LIST,
            data=json.dumps(note),
            **self.post_args,
            **self.create_user_header(mock_user)
        ), status=201)
        return note_json

    def _validate_fields(self, note_json):
        self.assertTrue("id" in note_json)
        self.assertTrue("title" in note_json)
        self.assertTrue("content" in note_json)
        self.assertTrue("tags" in note_json)

        self.assertTrue("created" in note_json)
        self.assertTrue("edited" in note_json)

        self.assertTrue("is_pinned" in note_json)
        self.assertTrue("is_archived" in note_json)

    def _validate_content(self, expected, actual):
        self.assertIsNotNone(actual["id"])
        self.assertEqual(expected["title"], actual["title"])
        self.assertEqual(expected["content"], actual["content"])

        self.assertEqual(len(expected["tags"]), len(actual["tags"]))
        for tag in expected["tags"]:
            self.assertTrue(tag in actual["tags"])
