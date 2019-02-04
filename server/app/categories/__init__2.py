# coding=utf-8

from app import components
from app.categories.model import Category


class CategoryService(components.Service):
    _model_class = Category

    def __init__(self):
        super().__init__()

    def fetch_all_items(self):
        return Category.select().where(Category.is_deleted == False).order_by(Category.order)
    pass


categoryService = CategoryService()


def init(app, api, models):
    from app.categories.controller import CategoryController, CategoryListController
    components.register_controllers(api, [CategoryController, CategoryListController])
    models.extend([Category])
    pass
