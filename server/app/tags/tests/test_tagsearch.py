from unittest import TestCase
import json
import ddt

print("name:", __name__)

from app import app
from components import BASE_PATH as API_BASE

@ddt.ddt
class TestTagsearch(TestCase):

    post_args = {
        'content_type': 'application/json'
    }
    
    def setUp(self):
        self.app = app.test_client()
        notes = [
            {
                'title': 'test_title',
                'content': 'test_content',
                'tags': ['these', 'are', 'the', 'test', 'tags', 'we', 'look', 'for']
            }, {
                'title': 'Test',
                'content': 'Contents',
                'tags': ['árvívz', 'tűrő', 'tükör', 'fúró', 'gép', 'zsiráf', 'oroszlán', 'gepárd']
            },
            {
                'title': 'Test',
                'content': 'Contents with unusal but valid tags',
                'tags': ['This is something we don\'t expect to see, but', 'we can have a tag like this', 'and it still sohuld be valid', 'as well']
            }
        ]
        
        for note in notes:
            response = self.app.post(API_BASE + '/notes/', data=json.dumps(note), **TestTagsearch.post_args)
            self.assertIsNotNone(response)
            self.assertEqual(201, response.status_code)
    
    @ddt.data(
        ('the', ['these', 'the']),
        ('these', ['these']),
        ('a', []),
        ('árv', ['árvívz'])
    )
    @ddt.unpack
    def  test_autocomplete_query(self, query, expected_result):
        # given (data) 
        query_string = {'q': query}

        # when
        response = self.app.get(API_BASE + '/tags/autocomplete/', query_string=query_string, **TestTagsearch.post_args)
        
        # then
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        response_json = json.loads(response.data)

        # for tag in self.expected_result['tags']:
            # self.assertTrue(tag in response_json['tags'])

        pass
