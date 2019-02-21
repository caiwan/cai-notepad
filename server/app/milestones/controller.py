# coding=utf-8

from flask_restful import request

from app import components, auth
from app.milestones import milestoneService


class MilestoneListController(components.Controller):
    path = "/milestones/"
    _service = milestoneService

    @auth.login_required
    def get(self):
        return self._fetch_all()

    @auth.login_required
    def post(self):
        return self._create(request.json)


class MilestoneController(components.Controller):
    path = "/milestones/<milestone_id>/"
    _service = milestoneService

    @auth.login_required
    def get(self, milestone_id):
        return self._read(milestone_id)

    @auth.login_required
    def put(self, milestone_id):
        return self._update(milestone_id)

    @auth.login_required
    def patch(self, milestone_id):
        return self._update(milestone_id)

    @auth.login_required
    def delete(self, milestone_id):
        return self._delete(milestone_id)
