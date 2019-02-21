# coding=utf-8
import logging

from collections import OrderedDict
import fuzzy
import Levenshtein
from slugify import slugify

from app import components
from app.tags.model import Tag, FuzzyTag


class TagService(components.Service):
    name = "tags"
    model_class = Tag
    settings = {
        "max-result": 10,
        "min-length": 3
    }

    def __init__(self):
        super().__init__()

    def fetch_all_items(self, search_query, result_limit):
        if search_query:
            return self.search_tags(search_query, result_limit)
        else:
            user_id = components.current_user_id()
            return Tag.select(Tag)\
                .join(components.BaseUser, on=(Tag.owner == components.BaseUser.id))\
                .where(components.BaseUser.id == user_id)\
                .objects()

    def serialize_item(self, item):
        return str(item.tag)

    def search_tags(self, search_query, result_limit):
        result_map = {}
        user_id = components.current_user_id()
        # I admit, it's ineffective in so many ways
        words = [word for word in self._make_fuzzy(
            search_query.split(" ")) if word]
        for word in words:
            tags_select = Tag.select(Tag)\
                .join(FuzzyTag)\
                .join(components.BaseUser, on=(Tag.owner == components.BaseUser.id))\
                .where(
                    FuzzyTag.fuzzy.contains(word),
                    components.BaseUser.id == user_id)
            for tag in tags_select:
                ld = Levenshtein.distance(str(tag.tag), search_query)
                if tag not in result_map or ld < result_map[tag]:
                    result_map[tag] = ld

        # order results by score
        result_map = OrderedDict((k, result_map[k]) for k in sorted(
            result_map, key=result_map.get))

        logging.debug(
            "result_set_distances=[{}]".format(
                ", ".join([str(k) + "=" + str(v)
                           for k, v in result_map.items()])
            )
        )

        if result_limit:
            return [tag for tag in result_map.keys()][:result_limit]
        return [tag for tag in result_map.keys()]

    def bulk_search_or_insert(self, tags):
        tag_set = set(tags)
        user_id = components.current_user_id()

        tag_items = set(
            Tag.select(Tag).join(components.BaseUser, on=(
                components.BaseUser.id == user_id))
            .where(
                Tag.tag << tag_set,
                Tag.owner.id == user_id
            ).objects())

        created_tags = []
        created_fuzzies = []
        # TODO: this part sucks for some reason:
        for new_tag in tag_set.difference(set(tag.tag for tag in tag_items)):
            (tag, fuzzies) = self._create_tag_from_string(new_tag)
            created_tags.append(tag)
            created_fuzzies.extend(fuzzies)

        with components.DB.atomic():
            user = components.current_user()
            if created_tags:
                for tag in created_tags:
                    tag.owner = user
                    tag.save()
                logging.debug(
                    "New tags:" + ", ".join([str(tag.tag) for tag in created_tags]))

            if created_fuzzies:
                for fuzzy_tag in created_fuzzies:
                    fuzzy_tag.save()
                logging.debug(
                    "New fuzzies:" + ", ".join([str(fuzzy.fuzzy) for fuzzy in created_fuzzies]))

        return list(tag_items) + created_tags

    def _create_tag_from_string(self, tag_str):
        tag = Tag(tag=tag_str)
        fuzzies = [FuzzyTag(tag=tag, fuzzy=fuzzy_word) for fuzzy_word in self._make_fuzzy(
            tag_str.split(" ")) if fuzzy_word]
        return (tag, fuzzies)

    _dmeta = fuzzy.DMetaphone()
    _nysiis = fuzzy.nysiis

    def _make_fuzzy(self, terms):
        for word in terms:
            slug = slugify(word).upper()
            yield slug
            dmeta = self._dmeta(slug)[0]
            yield dmeta.decode("utf-8") if dmeta else None
            yield self._nysiis(slug)


tagService = TagService()


class Module(components.Module):
    from app.tags.controller import TagAutoCompleteController
    name = "tags"
    services = [tagService]
    models = [Tag, FuzzyTag]
    controllers = [TagAutoCompleteController]


module = Module()
