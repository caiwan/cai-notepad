from flask import request
import components

from categories import CategoryService


class CategoryListController(components.Controller):
    """GET /api/categories/?tree=True will returns the categories as tree view"""
    path = "categories/"
    _service = CategoryService()

    def get(self):
        is_list_as_tree = request.args.get('tree').lower() == 'true'
        return self._fetch_all(is_list_as_tree)
    
    def post(self):
        return self._create(request.json)


class CategoryController(components.Controller):
    path = "categories/{category_id}"
    _service = CategoryService()

    def get(self, category_id):
        return self._read(category_id)

    def put(self, catagory_id):
        return self._update(item_id, request.json)

    def delete(self, category_id):
        return self._delete(item_id)
