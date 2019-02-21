# coding=utf-8

from flask_restful import request

from app import components, auth
from app.worklog import worklogService


class WorklogListController(components.Controller):
    path = "/worklogs/"
    _service = worklogService

    @auth.login_required
    def get(self):
        return self._fetch_all()

    @auth.login_required
    def post(self):
        return self._create(request.json)


class WorklogController(components.Controller):
    path = "/worklogs/<Worklog_id>/"
    _service = worklogService

    @auth.login_required
    def get(self, Worklog_id):
        return self._read(Worklog_id)

    @auth.login_required
    def put(self, Worklog_id):
        return self._update(Worklog_id)

    @auth.login_required
    def patch(self, Worklog_id):
        return self._update(Worklog_id)

    @auth.login_required
    def delete(self, Worklog_id):
        return self._delete(Worklog_id)
