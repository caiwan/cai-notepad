from unittest import TestCase
import json
import ddt
from chrono import Timer

import logging

import peewee

import app
from app import components
from app.tests import TestUtils

API_BASE = components.BASE_PATH


@ddt.ddt
class TestTagsearch(TestUtils, TestCase):

    TAGS_GET = components.BASE_PATH + "/tags/autocomplete/"
    NOTES_LIST = components.BASE_PATH + "/notes"

    post_args = {
        "content_type": "application/json"
    }

    def setUp(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.MODELS, safe=True)
        self.app = app.APP.test_client()

        notes = [
            {
                "title": "test_title",
                "content": "test_content",
                "tags": ["these", "are", "the", "test", "tags", "we", "look", "for"]
            }, {
                "title": "Test",
                "content": "Contents",
                "tags": ["árvívz", "tűrő", "tükör", "fúró", "gép", "zsiráf", "oroszlán", "gepárd"]
            },
            {
                "title": "Test",
                "content": "Contents with unusal but valid tags",
                "tags": ["This is something we don\"t expect to see, but", "we can have a tag like this", "and it still sohuld be valid", "as well"]
            }
        ]

        for note in notes:
            response = self.app.post(
                self.NOTES_LIST,
                data=json.dumps(note),
                **TestTagsearch.post_args,
                **self.create_user_header(TestUtils.REGULAR_USER)
                )
            self.assertEqual(201, response.status_code)

    def tearDown(self):
        self._db.close()

    @ddt.data(
        ("the", ["these", "the"]),
        ("these", ["these"]),
        ("xoxoxox", []),
        ("a", ["are", "árvívz"]),
        ("árv", ["árvívz"])
    )
    @ddt.unpack
    def test_autocomplete_query(self, query, expected_result):
        # given (data)
        query_string = {"q": query}

        # when
        with Timer() as timed:
            response = self.response(self.app.get(
                self.TAGS_GET,
                query_string=query_string,
                **self.post_args,
                **self.create_user_header(TestUtils.REGULAR_USER)
            ))

            # then
            logging.info("Queried tag:" + query)
            logging.info("Fetched tags:" + ", ".join([tag for tag in response]))
            logging.info("Time spent: {} ms".format(timed.elapsed * 1000))

            for tag in expected_result:
                self.assertTrue(tag in response)

        pass

    def test_autocomplete_rights(self):
        # given (data)
        query_string = {"q": "the"}

        # when
        # - query tags as another user
        with Timer() as timed:
            response = self.response(self.app.get(
                self.TAGS_GET,
                query_string=query_string,
                **self.post_args,
                **self.create_user_header(TestUtils.REGULAR_ALT_USER)
            ))

            # then
            # - You shall not recieve any response
            logging.info("Fetched tags:" + ", ".join([tag for tag in response]))
            logging.info("Time spent: {} ms".format(timed.elapsed * 1000))

            self.assertEqual(0, len(response))

