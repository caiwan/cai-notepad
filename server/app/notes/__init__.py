import sys

from flask import request
import components

import mongoengine


class Note(components.BaseModel):
    title = mongoengine.StringField(max_length=512)
    content = mongoengine.StringField()
    pass


class NoteListController(components.Controller):
    path = "/notes/"
    def get(self):
        note_json = [note.to_mongo() for note in Note.objects(is_deleted=False)]
        return(note_json, 200)

    def post(self):
        note_json = request.json
        if '_id' in note_json:
            del note_json['_id']

        note = components.BaseModel.update_document(Note(), note_json)
        note.save()
        return (note.to_mongo(), 201)

    pass


class NoteController(components.Controller):
    path = "/notes/<string:note_id>"

    def get(self, note_id):
        try: 
            note = Note.objects.get(_id=mongoengine.fields.ObjectId(note_id), is_deleted=False)
            return (note.to_mongo(), 200)

        except note.DoesNotExist as e:
            return({"error" : [str(e)]}, 404)
        except e:
            return({"error" : [str(e)]}, 500)

        return ('', 500)


    def put(self, note_id):
        note_json = request.json
        if '_id' in note_json:
            del note_json['_id']
        try: 
            task = Note.objects.get(_id=mongoengine.fields.ObjectId(note_id), is_deleted=False)
            components.BaseModel.update_document(task, note_json)
            # TODO: update modification date here 
            task.save()
            return (task.to_mongo(), 200)
        except Note.DoesNotExist as e:
            return({"error" : str(e)}, 404)
        except :
            return({
                "error" : [str(err) for err in sys.exc_info()]
            }, 500)
        return ('', 500)

    def delete(self, note_id):
        try: 
            note = Note.objects.get(_id=mongoengine.fields.ObjectId(note_id), is_deleted=False)
            note.is_deleted = True
            note.save()
        except Note.DoesNotExist as e:
            return({"error" : [str(e)]}, 404)
        except e:
            return({"error" : [str(e)]}, 500)

        return ('', 500)

    pass


def init(app, api, model_target):
    components.register_controllers(api, [NoteListController, NoteController])
