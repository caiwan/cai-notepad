# coding=utf-8

from flask import request

from app import auth
from app import components
from app.notes import NoteService


class NoteListController(components.Controller):
    path = "/notes/"
    _service = NoteService()

    @auth.login_required
    def get(self):
        category_filter = request.args.get("category", default="all", type=str)
        milestone_filter = request.args.get("milestone", default="all", type=str)
        return self._fetch_all(category_filter, milestone_filter)

    @auth.login_required
    def post(self):
        return self._create(request.json)

    pass


class NoteController(components.Controller):
    path = "/notes/<int:note_id>/"
    _service = NoteService()

    @auth.login_required
    def get(self, note_id):
        return self._read(note_id)

    @auth.login_required
    def put(self, note_id):
        return self._update(note_id, request.json)

    @auth.login_required
    def delete(self, note_id):
        return self._delete(note_id)

    pass
