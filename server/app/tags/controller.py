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
        search_query = request.args.get("q")
        result_limit = request.args.get("l")
        result_limit = 0 if not result_limit else int(result_limit)
        return self._fetch_all(search_query, result_limit)
