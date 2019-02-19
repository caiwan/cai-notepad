# import logging
from unittest import TestCase
import json
# from chrono import Timer

from app import components
from app.tests import TestUtils

API_BASE = components.BASE_PATH


class TestTaskCrud(TestUtils, TestCase):

    TASK_LIST = API_BASE + "/tasks/"
    TASK_GET = API_BASE + "/tasks/{id}/"

    def __init__(self, methodName):
        TestUtils.__init__(self)
        TestCase.__init__(self, methodName)

    def setUp(self):
        self._setup_app()

    def tearDown(self):
        self._db.close()

    def test_create(self):
        # given
        task = {"title": "My Title"}
        # when
        task_json = self._insert_task(task)
        # then
        self.assertEquals(task["title"], task_json["title"])

    def test_read(self):
        # given
        # - previously inserted task by an user
        task = {"title": "My Title"}
        task_json_post = self._insert_task(task)
        task_id = task_json_post["id"]

        # when
        # - read resource
        response = self.app.get(
            self.TASK_GET.format(id=task_id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER))
        self.assertEquals(200, response.status_code)
        task_json = json.loads(response.data)

        # then
        # - content matches
        self.assertEqual(task_id, task_json["id"])
        self.assertTrue("title" in task_json)
        self.assertEqual("My Title", task_json["title"])

    def test_update(self):
        # given
        # - previously inserted task by an user
        task = {"title": "My Title"}
        task_json_post = self._insert_task(task)
        task_id = task_json_post["id"]

        # when
        # - modify data
        edited_task = {"title": "My Edited Title"}
        response = self.app.put(
            self.TASK_GET.format(id=task_id),
            data=json.dumps(edited_task),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        )
        self.assertEquals(200, response.status_code)
        task_json = json.loads(response.data)

        # then
        # - data modified
        self.assertEqual(task_id, task_json["id"])
        self.assertTrue("title" in task_json)
        self.assertEqual("My Edited Title", task_json["title"])

    def test_delete(self):
        # given
        # - previously inserted task by an user
        task = {"title": "My Title"}
        task_json_post = self._insert_task(task)
        task_id = task_json_post["id"]

        # when
        # - delete
        response = self.app.delete(
            self.TASK_GET.format(id=task_id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        )
        self.assertEquals(200, response.status_code)

        # then
        # - no longer exists
        response = self.app.get(
            self.TASK_GET.format(id=task_id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER)
        )
        self.assertEquals(404, response.status_code)

    # Test access rights

    def test_list_rights(self):
        # given
        # - Tasks from two different user
        my_tasks = [self._insert_task({"title": "My Title %d" % i}, mock_user=TestUtils.REGULAR_USER) for i in range(3)]
        alt_tasks = [self._insert_task({"title": "Other My Title %d" % i}, mock_user=TestUtils.REGULAR_ALT_USER) for i in range(4)]

        # when
        # - They reads their own tasks
        my_tasks_response = self.app.get(
            self.TASK_LIST,
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_USER)
        )

        self.assertEquals(200, my_tasks_response.status_code)
        my_tasks_json = json.loads(my_tasks_response.data)

        alt_tasks_response = self.app.get(
            self.TASK_LIST,
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER)
        )

        self.assertEquals(200, alt_tasks_response.status_code)
        alt_tasks_json = json.loads(alt_tasks_response.data)

        # then
        # - There's no intersection between them
        self.assertEquals(len(my_tasks), len(my_tasks_json))
        self.assertEquals(len(alt_tasks), len(alt_tasks_json))
        for (sent, read) in zip(my_tasks + alt_tasks, my_tasks_json + alt_tasks_json):
            self.assertEqual(sent["title"], read["title"])

        my_ids = set([task["id"] for task in my_tasks_json])
        alt_ids = set([task["id"] for task in alt_tasks_json])
        self.assertFalse(bool(my_ids & alt_ids))

    def test_read_rights(self):
        # given
        # - previously inserted task by an user
        task = {"title": "My Title"}
        task_json_post = self._insert_task(task)
        task_id = task_json_post["id"]

        # when
        # - read resource by another user
        response = self.app.get(
            self.TASK_GET.format(id=task_id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER))

        # then
        # - requested content not found
        self.assertEquals(404, response.status_code)

    def test_update_rights(self):
        # given
        # - previously inserted task by an user
        task = {"title": "My Title"}
        task_json_post = self._insert_task(task)
        task_id = task_json_post["id"]

        # when
        # - read resource by another user
        edited_task = {"title": "My Edited Title"}
        response = self.app.put(
            self.TASK_GET.format(id=task_id),
            data=json.dumps(edited_task),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER))

        # then
        # - requested content not found
        self.assertEquals(404, response.status_code)

    def test_delete_rights(self):
        # given
        # - previously inserted task by an user
        task = {"title": "My Title"}
        task_json_post = self._insert_task(task)
        task_id = task_json_post["id"]

        # when
        # - read resource by another user
        response = self.app.delete(
            self.TASK_GET.format(id=task_id),
            **self.post_args,
            **self.create_user_header(TestUtils.REGULAR_ALT_USER))

        # then
        # - requested content not found
        self.assertEquals(404, response.status_code)

    # ---

    def _insert_task(self, task, mock_user=TestUtils.REGULAR_USER):
        response = self.app.post(
            self.TASK_LIST,
            data=json.dumps(task),
            **self.post_args,
            **self.create_user_header(mock_user)
        )
        self.assertEquals(201, response.status_code)
        task_json = json.loads(response.data)
        self.assertIsNotNone(task_json["id"])
        return task_json
