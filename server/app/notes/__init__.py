# coding=utf-8

import logging
import copy

import mongoengine

import components
from notes.model import Note
from tags import TagService


class NoteService(components.Service):
    _model_class = Note
    _tagService = TagService()

    def create_item(self, item_json):
        (note_json, tags) = self._select_and_sanitize_tags(item_json)
        item = Note.update_document(Note(tags=tags), item_json)
        item.save()
        return item

    def update_item(self, item_id, item_json):
        (item_json, tags) = self._select_and_sanitize_tags(item_json)
        item = Note.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
        Note.update_document(item, item_json)
        item.tags = tags
        item.changed()
        item.save()
        return item

    def serialize_item(self, item):
        json = item.to_mongo()
        json['tags'] = [tag.tag for tag in item.tags] 
        return json

    def _select_and_sanitize_tags(self, item_json):
        tags = []
        if 'tags' in item_json:
            tags = self._tagService.bulk_search_or_insert(item_json['tags'])
            del item_json['tags']
        logging.debug("Tags:" + ",".join([tag.tag for tag in tags]))
        return (item_json, tags)


# ----------------------------------------

def init(app, api, models):
    from notes.controller import NoteListController, NoteController
    components.register_controllers(api, [NoteListController, NoteController])
    models += [Note]
