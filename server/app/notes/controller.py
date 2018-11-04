import logging
from flask import request

import components
from notes import NoteService
from tags.model import Tag
from notes.model import Note

class NoteListController(components.Controller):
    path = "/notes/"
    _service = NoteService()

    def get(self):
        return self._fetch_all()

    def post(self):
        return self._create(request.json)

    pass


class NoteController(components.Controller):
    path = "/notes/<string:note_id>/"
    _service = NoteService()

    def get(self, note_id):
        return self._read(note_id)

    def put(self, note_id):
        return self._update(note_id, request.json)

    def delete(self, note_id):
        return self._delete(note_id)

    pass
