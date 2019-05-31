# coding=utf-8
import logging
import sys

from playhouse.shortcuts import dict_to_model, model_to_dict
from playhouse.shortcuts import Value

from app import components
from app.categories.model import Category

from app import utils


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
        ).order_by(Category.path)

    def create_item(self, item_json):
        parent = None
        if "parent" in item_json and item_json["parent"]:
            try:
                parent = self.read_item(item_json["parent"])
            except Category.DoesNotExist:
                raise components.BadRequestError()
            del item_json["parent"]

        user = components.current_user()
        count = 0
        if parent:
            count = len(parent.children)
        else:
            count = Category.select().join(
                components.BaseUser, on=(Category.owner == components.BaseUser.id)
            ).where(
                Category.parent.is_null(),
                Category.is_deleted == False,
                components.BaseUser.id == user.id
            ).count()

        path = self._fetch_path(parent.id if parent else None)
        path = "%s.%d" % (parent, count) if path else str(count)

        item = dict_to_model(Category, item_json)
        item.parent = parent
        item.order = count
        item.owner = user
        item.path = path
        item.save()
        return item

    def update_item(self, item_id, item_json):
        old_item = None
        try:
            old_item = self.read_item(item_id)
        except Category.DoesNotExist:
            raise components.ResourceNotFoundError()
        old_parent_id = old_item.parent.id if old_item.parent else None
        old_order = old_item.order

        parent = None
        if "parent" in item_json and item_json["parent"]:
            if item_json["parent"] == item_id:
                raise components.BadRequestError(
                    payload={"reason": "You can't be your own parent, you moron."})
            try:
                parent = self.read_item(item_json["parent"])
            except Category.DoesNotExist:
                raise components.BadRequestError()
            del item_json["parent"]

        parent_id = parent.id if parent else None

        item_json = self.sanitize_fields(item_json)
        item = dict_to_model(Category, item_json)

        path = self._fetch_path(parent.id if parent else None)
        path = "%s.%d" % (parent, item.order) if path else str(item.order)

        item.id = item_id
        item.parent = parent
        item.path = path
        item.save(only=item.dirty_fields)

        if (item.order != old_order) or (item.parent and item.parent.id != old_parent_id):
            user_id = components.current_user_id()
            self._reorder_branch(item, user_id=user_id, parent_id=parent_id)
            self._reorder_path(user_id=user_id, parent_id=parent_id)

            if item.parent and item.parent.id != old_parent_id:
                self._reorder_branch(None, user_id=user_id, parent_id=old_parent_id)
                self._reorder_path(user_id=user_id, parent_id=old_parent_id)

            # self._flatten_tree_order(user_id)

        return item

    def delete_item(self, item_id):
        from app.notes.model import Note
        from app.tasks.model import Task
        # from app.milestones.model import Milestone
        # from app.worklog.model import Worklog

        # --- delete -> merge all the stuff to its parents
        category = None
        try:
            category = self.read_item(item_id)
            # if category.parent:
            # parent = self.read_item(category.parent)
        except Category.DoesNotExist:
            raise components.ResourceNotFoundError()

        parent = category.parent

        # merge
        # We need to have an event dispatch-thingy to notify all the depending modules to move around
        user_id = components.current_user_id()
        with components.DB.atomic():
            for clazz in [
                Note, Task
                # , Milestone
            ]:
                # Why can't you just simply update?
                # clazz.update(
                #     category=parent,  # parent.id if parent else None,
                #     edited=datetime.now()
                # ).where(
                #     clazz.category == category,  # under normal circumstances, it can't be None
                # ).execute()
                for obj in clazz.select(
                    clazz
                ).join(
                    components.BaseUser, on=(clazz.owner == components.BaseUser.id)
                ).join(
                    Category, on=(clazz.category == Category.id)
                ).where(
                    clazz.category.id == category.id,  # under normal circumstances, it can't be None
                    clazz.owner.id == user_id
                ):
                    obj.category = parent
                    obj.changed()
                    obj.save()  # :/

            # Why can't you simply update?
            # Category.update(
            #     parent_id=parent.id,
            #     edited=datetime.now()
            # ).where(
            #     Category.parent == category,
            # ).execute()

            Parent = Category.alias()
            for child in Category.select(
                Category
            ).join(
                components.BaseUser, on=(Category.owner == components.BaseUser.id)
            ).join(
                Parent, on=(Category.parent == Parent.id)
            ).where(
                Parent.id == category.id,  # under normal circumstances, it can't be None
                Category.owner.id == user_id
            ):
                child.parent = parent
                child.changed()
                child.save()

            category.is_deleted = True
            category.changed()
            category.save()

            # TODO: recalculate path for parent
            # self._flatten_tree_order(user_id)
            return category

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

    def _fetch_path(self, item_id):
        if not item_id:
            return ""
        root_query = (Category
                      .select(Category.id, Category.parent_id, Category.order, Value(0).alias("level"))
                      .where(Category.id == item_id)
                      .cte(name="child", recursive=True))

        RTerm = Category.alias()
        recursive_query = (RTerm
                           .select(RTerm.id, RTerm.parent_id, RTerm.order, (root_query.c.level + 1).alias("level"))
                           .join(root_query, on=(RTerm.id == root_query.c.parent_id))
                           )

        cte = root_query.union_all(recursive_query)
        tree_query = cte.select_from(cte.c.id, cte.c.parent_id, cte.c.order, cte.c.level)

        items = [item.order for item in tree_query]
        items.reverse()
        path = ".".join("{:0>4}".format(utils.str_base(item, 32)) for item in items)
        logging.debug("Path: id=%d %s" % (item_id, path))
        return path

    def fetch_subtree(self, user_id, query_item_id):
        # http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery
        # http://docs.peewee-orm.com/en/latest/peewee/querying.html#common-table-expressions

        root_query = None
        if not query_item_id:
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

        tree_query = cte.select_from(cte.c.id, cte.c.order, cte.c.level)

        items = [item for item in tree_query]
        # logging.debug(" ".join(["id: %d level:%d order:%d \n" % (item.id, item.level, item.order) for item in items]))
        return Category.select().where(Category.id << [item.id for item in items]).order_by(Category.path)

    # TODO: Add as Celery task
    def _reorder_branch(self, item, user_id=None, parent_id=None):
        query = None
        # :/ This w=query sucks all the way through
        # if item:
        # if not item and parent_id:
        # elif user_id:
        #     query = (Category.select().join(components.BaseUser, on=(Category.owner == components.BaseUser.id))
        #              .where(Category.parent.id.is_null(), Category.owner.id == user_id))

        if item:
            # scenario #1: if
            # - item was given and it was put into a category
            # then
            # - select all the categories from its parent, except the given one
            query = None
            # - either category has parent or is at the root
            if (item.parent):
                query = Category.select(
                    Category
                ).join(
                    components.BaseUser, on=(Category.owner == components.BaseUser.id)
                ).where(
                    Category.parent_id == item.parent.id,
                    Category.id != item.id,
                    Category.is_deleted == False,
                    Category.owner.id == user_id
                )
            else:
                query = Category.select(
                    Category
                ).join(
                    components.BaseUser, on=(Category.owner == components.BaseUser.id)
                ).where(
                    Category.parent_id.is_null(),
                    Category.id != item.id,
                    Category.is_deleted == False,
                    Category.owner.id == user_id
                )
            pass
        else:
            if parent_id:
                # scenario #2: if
                # - item is none, but a parent id was given
                # then
                # - select all the items from that category
                query = (Category.select().join(
                    components.BaseUser, on=(Category.owner == components.BaseUser.id)
                ).where(
                    Category.parent_id == parent_id,
                    Category.is_deleted == False,
                    Category.owner.id == user_id
                ))
            elif user_id:
                # scenario #3: if
                # - item is none, and parent is none, but user is given
                # then
                # - select all the root items
                query = (Category.select().join(
                    components.BaseUser, on=(Category.owner == components.BaseUser.id)
                ).where(
                    Category.parent_id.is_null(),
                    Category.owner.id == user_id,
                    Category.is_deleted == False
                ))
                pass

        if query is None:
            raise ValueError("No item || user || parent_id given u=%s p=%s" % (
                str(user_id), str(parent_id)))

        categories = [category for category in query.execute()]
        if item:
            categories.insert(item.order, item)

        with components.DB.atomic():
            for (index, category) in zip(range(len(categories)), categories):
                category.order = index
                category.save(only=category.dirty_fields)
        pass

    def _reorder_path(self, user_id=None, parent_id=None):
        items = self.fetch_subtree(user_id, parent_id)

        if not user_id and not parent_id:
            raise ValueError("No item || user || parent_id given u=%s p=%s" % (
                str(user_id), str(parent_id)))

        with components.DB.atomic():
            for item in items:
                path = self._fetch_path(item.id)
                item.path = path
                item.save(only=item.dirty_fields)

    def serialize_item(self, item):
        try:
            return model_to_dict(
                item, exclude=[
                    Category.is_deleted,
                    Category.path,
                    Category.owner
                ], recurse=False)
        except:
            logging.exception(sys.exc_info()[0])
            raise

        pass

    def category_filter_helper(self, clazz, user_id, category_filter):
        if(str.isdigit(category_filter)):
            category_tree = self.fetch_subtree(user_id, int(category_filter))
            if not category_tree:
                raise components.ResourceNotFoundError()
            return [clazz.category_id << category_tree]
        elif (category_filter == "unassigned"):
            return [clazz.category_id.is_null()]
        elif (category_filter != "all"):
            raise components.BadRequestError()
        return []


categoryService = CategoryService()


def _flatten_all_categories():
    # Some dirty entity management script
    with components.DB.atomic():
        categories = {}
        for category in Category.select().order_by(Category.path):
            if category.parent_id not in categories:
                categories[category.parent_id] = []
            categories[category.parent_id].append(category)

        for group in categories.values():
            for (index, item) in zip(range(len(group)), group):
                item.order = index
                item.path = categoryService._fetch_path(item.id)
                logging.debug("Item: id=%d order=%d path=%s" % (item.id, item.order, item.path))
                item.save()


class Module(components.Module):
    from app.categories.controller import CategoryController, CategoryListController
    name = "categories"
    services = [categoryService]
    models = [Category]
    controllers = [CategoryController, CategoryListController]


module = Module()
