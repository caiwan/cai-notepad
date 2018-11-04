# coding=utf-8

import logging

from slugify import slugify 
import fuzzy
import Levenshtein

import components
from tags.model import Tag, FuzzyTag


class TagService(components.Service):
    _model_class = Tag


    def fetch_all_items(self, search_query, result_limit):
        return self.search_tag(search_query, result_limit)

    def serialize_item(self, item):
        return item.tag
        

    def search_tag(self, search_query, result_limit):
        terms = search_query.split(" ")
        result_map = {}
        # this not really gonna work I think
        for word in self._make_fuzzy(terms):
            fuzzies = FuzzyTag.objects(fuzzy__icontains=word)
            for fuzzy in fuzzies:
                if fuzzy.tag not in result_map:
                    result_map[fuzzy.tag] = Levenshtein.distance(word, fuzzy.fuzzy)

        # order by score
        result_map = dict((k,result_map[k]) for k in sorted(result_map, key=result_map.get, reverse=True))

        logging.debug(
            "Tag result set distances={" +
            ", ".join([ str(k.tag)+"="+str(v) for k, v in result_map.items()]) +
            "}"
        )
    
        if result_limit:
            return [tag for tag in result_map.keys()[:result_limit]]
        return [tag for tag in result_map.keys()]

    def bulk_search_or_insert(self, tags):
        new_tags = []
        tag_items = []
        for tag in tags:
            try:
                slug = slugify(tag)
                tag = Tag.objects.get(tag=tag)
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

        if created_tags:
            Tag.objects.insert(created_tags)
            logging.debug("New tags:" + ", ".join([tag.tag for tag in created_tags]))

        if created_fuzzies:
            FuzzyTag.objects.insert(created_fuzzies)
            logging.debug("New fuzzies:" + ", ".join([tag.fuzzy for tag in created_fuzzies]))

        return tag_items


    def _create_tag_from_string(self, tag_str):
        tag = Tag(tag=tag_str)
        fuzzies = []
        terms = tag_str.split(" ")
        for fuzzy_word in self._make_fuzzy(terms):
            fuzzies.append(FuzzyTag(tag=tag, fuzzy=fuzzy_word))
  
        return (tag, fuzzies)

    _dmeta = fuzzy.DMetaphone()
    _nysiis = fuzzy.nysiis

    def _make_fuzzy(self, terms):
        for word in terms:
            slug = slugify(word).upper()
            yield slug
            yield self._dmeta(slug)[0]
            yield self._nysiis(slug)


# ------------------------------------------------------------

def init(app, api, models):
    from tags.autocomplete import TagAutocomplete
    components.register_controllers(api, [TagAutocomplete])
    models.extend([Tag, FuzzyTag])
