# coding=utf-8

import components
from categories.model import Category

class CategoryService(components.Service):
    _model_class = Category
    pass


def init(app, api, models):
    from categories.controller import CategoryController, CategoryListController
    components.register_controllers(api, [CategoryListController, CategoryController])
    models += Category
