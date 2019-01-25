from unittest import TestCase
import json
from chrono import Timer 

import logging

import peewee

import app
import components

API_BASE= components.BASE_PATH

class TestTaskCrud(TestCase):

    post_args = {
        'content_type': 'application/json'
    }
    
    def setUp(self):
        self._db = peewee.SqliteDatabase(':memory:')
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.models, safe=True)
        self.app = app.app.test_client()
            
    def tearDown(self):
        self._db.close()

    def  test_create(self):
        # given
        task = {'title' : 'My Title'}
        # when
        task_json = self._insert_task(task)
        # then
        self.assertEquals(task['title'], task_json['title'])


    def  test_read(self):
        # given
        task = {'title' : 'My Title'}
        task_json_post = self._insert_task(task)
        task_id = task_json_post['id']

        # when
        task_json_get = self._get_task(task_id)

        # then
        # compare, I guess? 

    def  test_update(self):
        # given
        task = {'title' : 'My Title'}
        task_json_post = self._insert_task(task)
        task_id = task_json_post['id']
        task_json_get = self._get_task(task_id)

        # when
        edited_task = {'title' : 'My Edited Title'}
        response = self.app.put(API_BASE+'/tasks/'+str(task_id)+'/', data=json.dumps(edited_task), **self.post_args)
        self.assertEquals(200, response.status_code)
        task_json = json.loads(response.data)

        # then
        self.assertIsNotNone(task_json['id'])
        # compare, I guess? 
        
    def  test_delete(self):
        # given
        task = {'title' : 'My Title'}
        task_json_post = self._insert_task(task)
        task_id = task_json_post['id']
        task_json_get = self._get_task(task_id)

        # when
        response = self.app.delete(API_BASE+'/tasks/'+str(task_id)+'/', **self.post_args)
        self.assertEquals(200, response.status_code)

        # then
        response = self.app.get(API_BASE+'/tasks/'+str(id)+'/', **self.post_args)
        self.assertEquals(404, response.status_code)

    def _insert_task(self, task):
        response = self.app.post(API_BASE+'/tasks/', data=json.dumps(task), **self.post_args)
        self.assertEquals(201, response.status_code)
        task_json = json.loads(response.data)
        self.assertIsNotNone(task_json['id'])
        return task_json

    def _get_task(self, id):
        response = self.app.get(API_BASE+'/tasks/'+str(id)+'/', **self.post_args)
        self.assertEquals(200, response.status_code)
        task_json = json.loads(response.data)
        self.assertIsNotNone(task_json['id'])
        return task_json
