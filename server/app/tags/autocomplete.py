import logging
from flask import request
from slugify import slugify 
import components
from tags.model import Tag


class TagAutocomplete(components.Controller):
    """ GET /api/tags/autocomplete/?q=<tag> search for tag"""

    path = "/tags/autocomplete/"
    _model_class = Tag

    def get(self):
        search_query = request.args.get('q')
        tags = Tag.objects.search_text(slugify(search_query))

        logging.debug("Query: " + search_query + "; Found tags:" + ",".join([tag.tag for tag in tags]))

        return ('not implemented', 500)
