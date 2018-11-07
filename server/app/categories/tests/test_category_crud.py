from unittest import TestCase
import json

from app import app
from components import BASE_PATH as API_BASE


class TestCategoryCrud(TestCase):

    post_args = {
        'content_type': 'application/json'
    }

    def setUp(self):
        self.app = app.test_client()
    
    def test_add_category_wo_parent(self):
        # given
        category = {
            'title' : 'Category',
            'parent' : None
        }
        # when
        category_json = self._insert_category(category)
        
        # then
        self._validate_category()

    def test_add_category_w_parent(self):
        # given
        root_category = {
            'title' : 'Root Category',
            'parent' : None
        }
        root_category_json = self._insert_category(root_category)
        root_id = root_category_json['_id']

        child_categories = [{
            'title' : 'Child Category ' + i,
            'parent' : parent_id
        } for i in range (3)]

        # when
        child_categories_json = [self._insert_category(payload) for payload in child_categories]

        # then
        for pair in zip(child_categories, child_categories_json):
            self._validate_category(pair[0], pair[1])

        # - check parent-child relationship
        response = self.app.get(API_BASE+'/categories/'+root_id, **self.post_args)
        self.assertEquals(200, response.status_code)
        root_category_json = json.loads(response.data)
        self.assertTrue('children' in root_category_json)
        for child in child_categories_json:
            self.assertTrue(child['id'] in root_category_json['children'])


    def _insert_category(self, payload):
        response = self.app.post(API_BASE+'/categories/', data=json.dumps(payload), **self.post_args)
        self.assertEquals(201, response.status_code)
        category_json = json.loads(response.data)
        self.assertIsNotNone(note_id)
        return category_json

    def _validate_category(self, expected, actual):
        self.assertEqual(expected['title'], actual['title'])
        self.assertEqual(expected['parent'], actual['parent'])

