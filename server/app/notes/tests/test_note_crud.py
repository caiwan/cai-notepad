from unittest import TestCase
import json
import logging

from app import app
from components import BASE_PATH as API_BASE

class TestNotes(TestCase):

    post_args = {
        'content_type': 'application/json'
    }
    
    new_note = {
        'title': 'test_title',
        'content': 'test_content\r\nárviz tűrő tükör fúró gép\r\n',
        'tags': ['these', 'are', 'the', 'test', 'tags', 'we', 'look', 'for', 'árviz', 'tűrő', 'tükör', 'fúró', 'gép']
    }

    edited_note = {
        'title': 'edited title',
        'content': 'edited contents',
        'tags': ['these', 'are', 'the', 'other', 'tags', 'we', 'have', 'edited', 'so', 'far']
    }

    def setUp(self):
        self.app = app.test_client()

    def  test_create_note(self):
        # given
        # - fixture

        #when
        response = self.app.post(API_BASE + '/notes/', data=json.dumps(self.new_note), **TestNotes.post_args)

        #then
        self.assertIsNotNone(response)
        self.assertEqual(201, response.status_code)

        response_json = json.loads(response.data)

        self.assertTrue('_id' in response_json)
        self.assertTrue('_cls' in response_json)
        self._validate_tags(self.new_note, response_json)
        # TODO validate content

        

    def test_read_note(self):
        # given
        note_id = self._insert_note(self.new_note)

        #when
        response = self.app.get("{}/notes/{}/".format(API_BASE, note_id), **TestNotes.post_args)

        #then
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)

        response_json = json.loads(response.data)

        self._validate_tags(self.new_note, response_json)
        # TODO validate content


    def test_delete_note(self):
        # given
        note_id = self._insert_note(self.new_note)

        #when
        response = self.app.delete("{}/notes/{}/".format(API_BASE, note_id), **TestNotes.post_args)
        self.assertIsNotNone(response)
        self.assertEqual(201, response.status_code)

        #then
        response = self.app.get("{}/notes/{}/".format(API_BASE, note_id), **TestNotes.post_args)
        self.assertIsNotNone(response)
        self.assertEqual(404, response.status_code)

    def test_edit_note(self):
        # given 
        # - fixture, and
        note_id = self._insert_note(self.new_note)

        #when 
        response = self.app.put("{}/notes/{}/".format(API_BASE, note_id), data=json.dumps(self.edited_note), **TestNotes.post_args)

        #then
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)

        response_json = json.loads(response.data)

        self._validate_tags(self.edited_note, response_json)


    def _insert_note(self, note):
        response = self.app.post(API_BASE + '/notes/', data=json.dumps(note), **TestNotes.post_args)

        self.assertIsNotNone(response)
        self.assertEqual(201, response.status_code)

        response_json = json.loads(response.data)
        note_id = response_json['_id']
        self.assertIsNotNone(note_id)
        logging.debug('note_id={}'.format(note_id))
        return note_id

    def _validate_tags(self, expected, actual):
        self.assertEqual(len(expected['tags']), len(actual['tags']))
        for tag in expected['tags']:
            self.assertTrue(tag in actual['tags'])
