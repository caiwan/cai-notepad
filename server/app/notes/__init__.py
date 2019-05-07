# coding=utf-8

import logging
# import copy

import markupsafe
from playhouse.shortcuts import dict_to_model, model_to_dict

from app import components
from app.notes.model import Note, TaggedNote
from app.tags import tagService
from app.categories import categoryService


class NoteService(components.Service):
    name = "notes"
    model_class = Note

    def __init__(self):
        super().__init__()

    def fetch_all_items(self, category_filter, milestone_filter):
        user_id = components.current_user_id()
        query = Note.select(Note)
        # .join(
        #   components.BaseUser, on=(Note.owner == components.BaseUser.id)
        # )

        category_select = []
        if (category_filter == "all"):
            pass
        elif (category_filter == "unassigned"):
            category_select = [Note.category_id.is_null()]
            pass
        else:
            category_tree = categoryService.fetch_subtree(user_id, int(category_filter))
            if not category_tree:
                raise components.ResourceNotFoundError()
            category_select = [Note.category_id << category_tree]
            pass

        milestone_select = []
        # milestone_filter == "all"
        # milestone_filter == "unassigned"
        # else ...

        return query.where(
            Note.is_deleted == False,
            *category_select,
            *milestone_select,
            Note.owner_id == user_id
        ).order_by(Note.edited.desc()).objects()

    def create_item(self, item_json):
        (item_json, tags) = self._select_and_sanitize_tags(item_json)

        # Check if user has ownership over the category given
        if (item_json["category"] and not categoryService.read_item(item_json["category"])):
            raise components.BadRequestError()

        item = dict_to_model(Note, item_json)
        item.content = markupsafe.escape(markupsafe.Markup(item.content))
        item.owner = components.current_user()
        item.save(force_insert=True)
        item.tags.add(tags)
        return item

    def update_item(self, item_id, item_json):
        myItem = self.read_item(item_id)
        (item_json, tags) = self._select_and_sanitize_tags(item_json)
        item = dict_to_model(Note, item_json)
        with components.DB.atomic():
            item.id = int(myItem.id)
            item.changed()
            item.save()
            item.tags.clear()
            item.tags.add(tags)
            return item
        raise RuntimeError("Could not update note")

    def serialize_item(self, item):
        item_json = model_to_dict(item, exclude=(
            Note.is_deleted,
            Note.owner,
            Note.tags
        ), recurse=False)
        tags = [tag for tag in item.tags]
        item_json["tags"] = [tag.tag for tag in tags]
        return item_json

    def _select_and_sanitize_tags(self, item_json):
        tags = []
        item_json = self.sanitize_fields(item_json)
        if "tags" in item_json:
            tags = tagService.bulk_search_or_insert(item_json["tags"])
            del item_json["tags"]
        logging.debug("Selected tags:" + ",".join([tag.tag for tag in tags]))
        return (item_json, tags)


noteService = NoteService()

# ----------------------------------------


class Module(components.Module):
    from app.notes.controller import NoteListController, NoteController
    name = "notes"
    services = [noteService]
    models = [Note, TaggedNote]
    controllers = [NoteListController, NoteController]


module = Module()
