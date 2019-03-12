# coding=utf-8
import logging
import sys
import json

from playhouse.shortcuts import dict_to_model, model_to_dict
from playhouse.shortcuts import Value

from app import components
from app.categories.model import Category

import logging


class CategoryService(components.Service):
    name = "categories"
    model_class = Category

    def fetch_all_items(self):
        user_id = components.current_user_id()
        return Category.select(Category).join(
            components.BaseUser, on=(Category.owner == components.BaseUser.id)
        ).where(
            Category.is_deleted == False,
            components.BaseUser.id == user_id
        ).order_by(Category.flatten_order)

    def create_category(self, item_json):
        parent = None
        if "parent" in item_json and item_json["parent"]:
            parent = self.read_item(item_json["parent"])
            del item_json["parent"]

        item = dict_to_model(Category, item_json)
        item.parent = parent
        item.owner = components.current_user()
        item.save()
        return item

    def _create_item(self, item_json):
        # when bulk-inserting multiple items please use _create_item
        # then call _flatten_tree_order() when database structure is ready
        # to avoid unnecessary load
        item = self.create_category(item_json)
        self._flatten_tree_order()
        return item

    def _edit_category(self, item_id, item_json):
        parent = None
        if "parent" in item_json and item_json["parent"]:
            parent = self.read_item(int(item_json["parent"]))
            del item_json["parent"]

        item = dict_to_model(Category, item_json)
        item.parent = parent
        item.save()
        return item

    def update_item(self, item_id, item_json):
        old_item = self.read_item(item_id)
        old_parent_id = None
        if old_item.parent:
            old_parent_id = old_item.parent.id
        old_order = old_item.order

        item = self._edit_category(self, item_json)

        # rearrange if structure changed
        if item.order != old_order or (item.parent and item.parent.id != old_parent_id):
            self._flatten_tree_order()

        return item

    def merge_category(self, src_id, dst_id):
        # TBD
        pass

    def find_by_name(self, query_name):
        try:
            return Category.get(
                Category.name.contains(query_name.lower()),
                Category.is_deleted == False,
            )
        except Category.DoesNotExist:
            return None

    def fetch_all_by_name(self, query_name):
        return Category.select().where(
            Category.name.contains(query_name),
            Category.is_deleted == False,
        )

    def fetch_subtree_ids(self, query_item_id):
        # http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery
        # http://docs.peewee-orm.com/en/latest/peewee/querying.html#common-table-expressions

        root_query = None
        if query_item_id is None:
            root_query = (Category
                          .select(Category.id, Category.order, Value(0).alias("level"))
                          .where(Category.parent.is_null())
                          .cte(name="roots", recursive=True))
        else:
            root_query = (Category
                          .select(Category.id, Category.order, Value(0).alias("level"))
                          .where(Category.parent.id == query_item_id)
                          .cte(name="roots", recursive=True))

        RTerm = Category.alias()
        recursive_query = (RTerm
                           .select(RTerm.id, RTerm.order, (root_query.c.level + 1).alias("level"))
                           .join(root_query, on=(RTerm.parent == root_query.c.id))
                           )

        cte = root_query.union_all(recursive_query)

        tree_query = (cte
                      .select_from(cte.c.id, cte.c.order, cte.c.level)
                      .order_by(cte.c.id)
                      )

        return tree_query

    def fetch_subtree(self, query_item_id):
        tree_query = self.fetch_subtree_ids(query_item_id)
        return Category.select().where(Category.id << [item.id for item in tree_query])

    def fetch_subtree_ordered(self, query_item_id):
        result_query = self.fetch_subtree(query_item_id)
        result_map = dict((item.id, item) for item in result_query)

        # build tree
        tree_ids = {}
        root_item_ids = []
        for item in result_query:
            if not item.parent or item.parent.id == query_item_id:
                root_item_ids.append(item.id)

            parent_id = item.parent.id if item.parent else 0
            if parent_id not in tree_ids:
                tree_ids[parent_id] = [item.id]
            else:
                tree_ids[parent_id].append(item.id)

        # logging.info("root: {}".format(" ,".join(str(o) for o in root_item_ids)))
        # for (k,v) in tree_ids.items():
        #     logging.info("kv: {}:[{}]".format(str(k),", ".join(str(o) for o in v)))

        # reorder it in preorder travelsal
        result = []

        queue = root_item_ids[::-1]
        while queue:
            item_id = queue.pop()
            result.append(result_map[item_id])

            if item_id in tree_ids:
                queue.extend(tree_ids[item_id][::-1])

        return (len(result), result)

    # TODO: Add Celery task
    def _flatten_tree_order(self):
        (count, items) = self.fetch_subtree_ordered(None)
        with components.DB.atomic():
            for (index, item) in zip(range(count), items):
                item.flatten_order = index
                item.save()
        pass

    def bulk__create_items(self, items_json):
        parent_map = dict()
        item_map = dict()
        items = []
        with components.DB.atomic():
            for item_json in items_json:

                if "id" not in item_json:
                    raise RuntimeError("ID is missing from one item")

                id = int(item_json["id"])

                parent_id = None

                if "parent" in item_json and item_json["parent"]:
                    parent_id = int(
                        item_json["parent"]["id"]) if "id" in item_json["parent"] else None

                del item_json["id"]
                del item_json["parent"]

                parent_map[id] = parent_id

                item = self.create_category(item_json)
                item_map[id] = item
                items.append(item)

            for (item_id, parent_id) in parent_map.items():
                if parent_id:
                    item = item_map[item_id]
                    item.parent = item_map[parent_id]
                    item.save()

            self._flatten_tree_order()

            return items
        pass

    def serialize_item(self, item):
        try:
            return model_to_dict(
                item, exclude=[
                    Category.is_deleted,
                    Category.flatten_order,
                    Category.owner
                ], recurse=False)
        except:
            logging.exception(sys.exc_info()[0])
            raise

        pass


categoryService = CategoryService()


class Module(components.Module):
    from app.categories.controller import CategoryController, CategoryListController
    name = "categories"
    services = [categoryService]
    models = [Category]
    controllers = [CategoryController, CategoryListController]


module = Module()
