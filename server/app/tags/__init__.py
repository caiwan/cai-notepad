# coding=utf-8

import logging


import components
from tags.model import Tag
from slugify import slugify 


class TagService(components.Service):
    _model_class = Tag

    def bulk_search_or_insert(self, tags):
        new_tags = []
        tag_items = []
        for tag in tags:
            try:
                slug = slugify(tag)
                tag = Tag.objects.get(slug=slug)
                tag_items.append(tag)
            except Tag.DoesNotExist as e:
                new_tags.append(tag)
            except Exception as e:
                raise RuntimeError(e)

        created_tags = []
        for new_tag in new_tags:
            tag = self._create_tag_from_string(new_tag)
            created_tags.append(tag)
            tag_items.append(tag)

        if created_tags:
            Tag.objects.insert(created_tags)

        return tag_items

    def _create_tag_from_string(self, tag):
        return Tag(tag=tag, slug=slugify(tag))


# ------------------------------------------------------------

def init(app, api, models):
    from tags.autocomplete import TagAutocomplete
    components.register_controllers(api, [TagAutocomplete])
    models += [Tag]
