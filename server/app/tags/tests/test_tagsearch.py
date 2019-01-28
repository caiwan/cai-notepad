from unittest import TestCase
import json
import ddt
from chrono import Timer

import logging

import peewee

import app
from app import components

API_BASE = components.BASE_PATH


@ddt.ddt
class TestTagsearch(TestCase):

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
            response = self.app.post(API_BASE + "/notes/", data=json.dumps(note), **TestTagsearch.post_args)
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
            response = self.app.get(API_BASE + "/tags/autocomplete/", query_string=query_string, **TestTagsearch.post_args)

        # then
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)

        logging.info("Queryed tag:" + query)
        logging.info("Fetched tags:" + ", ".join([tag for tag in response_json]))
        logging.info("Time spent: {} ms".format(timed.elapsed * 1000))

        for tag in expected_result:
            self.assertTrue(tag in response_json)

        pass
