# coding=utf-8

import components
from categories.model import Category

class CategoryService(components.Service):
    _model_class = Category

    def fetch_all_items(self):
        return Category.select().where(Category.is_deleted == False).order_by(Category.order)
    pass


def init(app, api, models):
    from categories.controller import CategoryController, CategoryListController
    components.register_controllers(api, [CategoryController, CategoryListController])
    models.extend([Category])
    pass
