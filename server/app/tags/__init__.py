# coding=utf-8

import logging

import fuzzy
import Levenshtein
from slugify import slugify 

import components
from tags.model import Tag, FuzzyTag

class TagService(components.Service):
    _model_class = Tag

    def fetch_all_items(self, search_query, result_limit):
        if search_query :
            return self.search_tags(search_query, result_limit)
        return Tag.select()

    def serialize_item(self, item):
        return str(item.tag)
    
    def search_tags(self, search_query, result_limit):
        result_map = {}

        # I admit, it's ineffective in so many ways
        words = [word for word in self._make_fuzzy(search_query.split(" ")) if word]
        fuzzies = []
        for word in words :
            fuzzy = FuzzyTag.select().where(FuzzyTag.fuzzy.contains(word)).objects()
            fuzzies.extend(fuzzy)

        for fuzzy in fuzzies:
            ld = Levenshtein.distance(str(fuzzy.tag.tag), search_query)
            if fuzzy.tag not in result_map or ld > result_map[fuzzy.tag]:
                result_map[fuzzy.tag] = ld

        # order results by score
        result_map = dict((k,result_map[k]) for k in sorted(result_map, key=result_map.get))

        logging.debug(
            "resut_set_distances={" +
            ", ".join([ str(k.tag)+"="+str(v) for k, v in result_map.items()]) +
            "}"
        )
    
        if result_limit:
            return  [tag for tag in result_map.keys()][:result_limit]
        return [tag for tag in result_map.keys()]

    def bulk_search_or_insert(self, tags):
        new_tags = []
        tag_items = []
        for tag in tags:
            try:
                tag = Tag.get(Tag.tag == tag)
                tag_items.append(tag)
            except Tag.DoesNotExist as e:
                new_tags.append(tag)

        created_tags = []
        created_fuzzies = []
        for new_tag in new_tags:
            (tag, fuzzies) = self._create_tag_from_string(new_tag)
            created_tags.append(tag)
            tag_items.append(tag)
            created_fuzzies.extend(fuzzies)

        with components.DB.atomic():
            if created_tags:
                for tag in created_tags:
                    tag.save()
                logging.debug("New tags:" + ", ".join([str(tag.tag) for tag in created_tags]))

            if created_fuzzies:
                for fuzzy_tag in created_fuzzies:
                    fuzzy_tag.save()
                logging.debug("New fuzzies:" + ", ".join([str(fuzzy.fuzzy) for fuzzy in created_fuzzies]))

        return tag_items

    def _create_tag_from_string(self, tag_str):
        tag = Tag(tag=tag_str)
        fuzzies = [FuzzyTag(tag=tag, fuzzy=fuzzy_word) for fuzzy_word in self._make_fuzzy(tag_str.split(" ")) if fuzzy_word]
        return (tag,fuzzies)

    _dmeta = fuzzy.DMetaphone()
    _nysiis = fuzzy.nysiis

    def _make_fuzzy(self, terms):
        for word in terms:
            slug = slugify(word).upper()
            yield slug
            dmeta = self._dmeta(slug)[0]
            yield dmeta.decode("utf-8") if dmeta else None
            yield self._nysiis(slug)

def init(app, api, models):
    from tags.controller import TagAutoCompleteController
    components.register_controllers(api, [TagAutoCompleteController])
    models.extend([Tag, FuzzyTag])
    pass
