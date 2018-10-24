import sys

from flask import request
import components

import mongoengine


class Note(components.BaseModel):
    title = mongoengine.StringField(max_length=512)
    content = mongoengine.StringField()
    is_archived = mongoengine.BooleanField(default=False)
    is_pinned = mongoengine.BooleanField(default=False)
    pass


class NoteListController(components.Controller):
    path = "/notes/"
    def get(self):
        return self._fetch_all(Note)

    def post(self):
        return self._create(Note, request)

    pass


class NoteController(components.Controller):
    path = "/notes/<string:note_id>/"

    def get(self, note_id):
        return self._read(Note, note_id)

    def put(self, note_id):
        return self._update(Note, request, note_id)

    def delete(self, note_id):
        return self._delete(Note, note_id)

    pass


def init(app, api, model_target):
    components.register_controllers(api, [NoteListController, NoteController])
