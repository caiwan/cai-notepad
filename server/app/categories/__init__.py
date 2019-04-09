# coding=utf-8
import logging
import sys

from playhouse.shortcuts import dict_to_model, model_to_dict
from playhouse.shortcuts import Value

from app import components
from app.categories.model import Category


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

        if parent and parent.id == item_id:
            raise components.BadRequestError(
                payload={"reason": "You can't be your own parent, you moron."})

        item_json = self.sanitize_fields(item_json)

        item = dict_to_model(Category, item_json)
        item.id = item_id
        item.parent = parent
        item.save()
        return item

    def update_item(self, item_id, item_json):
        old_item = self.read_item(item_id)
        old_parent_id = old_item.parent.id if old_item.parent else None
        old_order = old_item.order

        item = self._edit_category(old_item.id, item_json)

        # rearrange if structure changed
        # TODO: -> Celery
        if (item.order != old_order) or (item.parent and item.parent.id != old_parent_id):
            user_id = components.current_user_id()
            self._reorder_branch(
                user_id=user_id, parent_id=item.parent.id if item.parent else None)
            if item.parent and item.parent.id != old_parent_id:
                self._reorder_branch(user_id=user_id, parent_id=old_parent_id)

            self._flatten_tree_order(user_id)

        return item

    def merge_category(self, src_id, dst_id):
        # TBD
        # - Merges all the that that belongs to a tasks from src to dst
        # - Check if dst is not parent of src, neither in it's ancestors

        # Merge notes
        # Merge tasks
        # RM Src task
        # Reload shitz maybe on client?
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

    def fetch_subtree_ids(self, user_id, query_item_id):
        # http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery
        # http://docs.peewee-orm.com/en/latest/peewee/querying.html#common-table-expressions

        root_query = None
        if query_item_id is None:
            root_query = (Category
                          .select(Category.id, Category.order, Value(0).alias("level"))
                          .join(components.BaseUser, on=(Category.owner == components.BaseUser.id))
                          .where(Category.parent.is_null(), Category.owner.id == user_id)
                          .cte(name="roots", recursive=True))
        else:
            root_query = (Category
                          .select(Category.id, Category.order, Value(0).alias("level"))
                          .join(components.BaseUser, on=(Category.owner == components.BaseUser.id))
                          .where(Category.parent.id == query_item_id, Category.owner.id == user_id)
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

    def fetch_subtree(self, user_id, query_item_id):
        tree_query = self.fetch_subtree_ids(user_id, query_item_id)
        return Category.select().where(Category.id << [item.id for item in tree_query])

    def fetch_subtree_ordered(self, user_id, query_item_id):
        result_query = self.fetch_subtree(user_id, query_item_id)
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

    # TODO: Add as Celery task
    def _flatten_tree_order(self, user_id):
        (count, items) = self.fetch_subtree_ordered(user_id, None)
        with components.DB.atomic():
            for (index, item) in zip(range(count), items):
                item.flatten_order = index
                item.save()
        pass

    # TODO: Add as Celery task
    def _reorder_branch(self, user_id=None, parent_id=None):
        query = None
        if parent_id:
            query = (Category.select()
                     .where(Category.parent.id == parent_id))
        elif user_id:
            query = (Category.select().join(components.BaseUser, on=(Category.owner == components.BaseUser.id))
                     .where(Category.parent.id.is_null(), Category.owner.id == user_id))

        if query is None:
            raise RuntimeError("No user || parent_id given u=%s p=%s" % (
                str(user_id), str(parent_id)))

        with components.DB.atomic():
            for (index, category) in zip(range(query.count()), query.execute()):
                category.order = index
                category.save()

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


def _flatten_all_categories():
    # Some dirty entity management script
    with components.DB.atomic():
        for user in components.BaseUser.select():
            categoryService._flatten_tree_order(user.id)

        categories = {}
        for category in Category.select().order_by(Category.flatten_order):
            if category.parent_id not in categories:
                categories[category.parent_id] = []
            categories[category.parent_id].append(category)

        for group in categories.values():
            for (index, item) in zip(range(len(group)), group):
                item.order = index
                item.save()


class Module(components.Module):
    from app.categories.controller import CategoryController, CategoryListController
    name = "categories"
    services = [categoryService]
    models = [Category]
    controllers = [CategoryController, CategoryListController]


module = Module()
