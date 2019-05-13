from flask import request

from app import components
from app import auth
from app.categories import categoryService


class CategoryListController(components.Controller):
    path = "/categories/"
    _service = categoryService

    @auth.login_required
    def get(self):
        return self._fetch_all()

    @auth.login_required
    def post(self):
        return self._create(request.json)


class CategoryController(components.Controller):
    path = "/categories/<int:category_id>/"
    _service = categoryService

    @auth.login_required
    def get(self, category_id):
        return self._read(category_id)

    @auth.login_required
    def put(self, category_id):
        return self._update(category_id, request.json)

    @auth.login_required
    def delete(self, category_id):
        return self._delete(category_id)
