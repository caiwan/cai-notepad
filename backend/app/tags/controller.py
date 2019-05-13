from flask import request
from app import components, auth
from app.tags import tagService


class TagAutoCompleteController(components.Controller):
    """
    GET /api/tags/autocomplete/?q=<tag> search for tag
    GET /api/tags/autocomplete/?q=<tag>%l=<n> yields the top n results or less
    """

    path = "/tags/autocomplete/"
    _service = tagService

    @auth.login_required
    def get(self):
        search_query = request.args.get("q", default="", type=str)
        result_limit = request.args.get("l", default=0, type=int)
        return self._fetch_all(search_query, result_limit)
