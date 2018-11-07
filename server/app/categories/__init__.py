# coding=utf-8

import components
from categories.model import Category

class CategoryService(components.Service):
    _model_class = Category

    def fetch_all_items(self):
        return Category.objects(is_deleted=False).order_by('-order')

    def read_item(self, item_id):
        return Category.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)

    def create_item(self, item_json):
        item = Category.update_document(self._model_class(), item_json)
        item.save()
        return item

    def update_item(self, item_id, item_json):
        item = Category.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
        BaseModel.update_document(item, item_json)
        item.changed()
        item.save()
        return item

    def delete_item(self, item_id):
        item = Category.objects.get(_id=mongoengine.fields.ObjectId(item_id), is_deleted=False)
        item.is_deleted = True
        item.changed()
        item.save()

    def serialize_item(self, item):
        return item.to_mongo()

    pass


def init(app, api, models):
    from categories.controller import CategoryController, CategoryListController
    components.register_controllers(api, [CategoryController, CategoryListController])
    models.extend([Category])
    pass
