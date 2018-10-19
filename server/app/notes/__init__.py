import sys

from flask import request
import components

import mongoengine


# model goez somewhere around here

class NoteListController(components.Controller):
    path = "/notes/"
    def get(self):
        pass

    def post(self):
        pass

    pass


class NoteController(components.Controller):
    path = "/notes/<string:note_id>"

    def get(self, note_id):
        pass

    def put(self, note_id):
        pass

    def delete(self, note_id):
        pass

    pass


def init(app, api, model_target):
    components.register_controllers(api, components.Controller.__subclasses__())
