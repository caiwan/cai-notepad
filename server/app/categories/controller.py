from flask import request
import components

from categories import categoryService


class CategoryListController(components.Controller):
    path = "/categories/"
    _service = categoryService

    def get(self):
        return self._fetch_all()
    
    def post(self):
        return self._create(request.json)


class CategoryController(components.Controller):
    path = "/categories/<int:category_id>/"
    _service = categoryService

    def get(self, category_id):
        return self._read(category_id)

    def put(self, category_id):
        return self._update(category_id, request.json)

    def delete(self, category_id):
        return self._delete(category_id)
