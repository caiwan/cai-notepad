# coding=utf-8

import logging
import copy

import peewee
from playhouse.shortcuts import *

import components
from notes.model import Note, TaggedNote
from tags import TagService


class NoteService(components.Service):
    _model_class = Note
    _tagService = TagService()

    def fetch_all_items(self):
        return Note.select().where(Note.is_deleted == False).order_by(Note.edited.desc())

    def create_item(self, item_json):
        (item_json, tags) = self._select_and_sanitize_tags(item_json)
        # Category ?
        item = dict_to_model(Note, item_json)
        item.save(force_insert=True)
        item.tags.add(tags)
        return item

    def update_item(self, item_id, item_json):
        (item_json, tags) = self._select_and_sanitize_tags(item_json)
        item = dict_to_model(Note, item_json)
        with components.DB.atomic():
            item.id = int(item_id)
            item.changed()
            item.update()
            item.tags.clear()
            item.tags.add(tags)
            return item
        raise RuntimeError("Could not update")

    def serialize_item(self, item):
        json = model_to_dict(item, exclude=['tags'])
        tags = [tag for tag in item.tags]
        json['tags'] = [tag.tag for tag in item.tags] 
        return json

    def _select_and_sanitize_tags(self, item_json):
        tags = []
        item_json = self.sanitize_fields(item_json)
        if 'tags' in item_json:
            tags = self._tagService.bulk_search_or_insert(item_json['tags'])
            del item_json['tags']
        logging.debug("Selected tags:" + ",".join([tag.tag for tag in tags]))
        return (item_json, tags)


# ----------------------------------------

def init(app, api, models):
    from notes.controller import NoteListController, NoteController
    components.register_controllers(api, [NoteListController, NoteController])
    models += [Note, TaggedNote]
