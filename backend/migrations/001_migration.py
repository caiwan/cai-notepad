"""Peewee migrations -- 001_migration.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

from datetime import datetime, date, time
from uuid import uuid4
import peewee

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = peewee.SQL


def migrate(migrator, database, fake=False, **kwargs):

    class BaseModel(peewee.Model):
        pass

    @migrator.create_model
    class Role(peewee.Model):
        name = peewee.TextField(null=False, unique=True)
        pass

    @migrator.create_model
    class User(BaseModel):
        class Meta:
            table_name = "users"
        name = peewee.TextField(null=False, unique=True)
        password = peewee.TextField(null=False)
        display_name = peewee.TextField(null=True)
        created = peewee.DateTimeField(null=False, default=datetime.now, formats=["%s"])
        edited = peewee.DateTimeField(null=False, default=datetime.now, index=True, formats=["%s"])
        user_ref_id = peewee.UUIDField(null=False, unique=True, index=True, default=uuid4)
        is_deleted = peewee.BooleanField(null=False, default=False)
        is_active = peewee.BooleanField(null=False, default=False)
        permissions = peewee.ManyToManyField(Role, backref="users")

    migrator.create_model(User.permissions.through_model)

    @migrator.create_model
    class Token(BaseModel):
        user = peewee.ForeignKeyField(User)
        issued_at = peewee.DateTimeField(null=False, default=datetime.now, formats=["%s"])
        expiration = peewee.DateTimeField(null=False, formats=["%s"])
        jwt = peewee.TextField(null=False)

    # User setting tables
    @migrator.create_model
    class UserAuthenticator(BaseModel):
        owner = peewee.ForeignKeyField(User, backref="authenticators")
        is_deleted = peewee.BooleanField(null=False, default=False)
        idp_id = peewee.TextField(null=False)
        access_token = peewee.TextField(null=False)
        id_token = peewee.TextField(null=False)
        token_type = peewee.TextField(null=False, default="Bearer")
        expires_at = peewee.DateTimeField(null=False, formats=["%s"])
        profile = peewee.TextField(null=False)

    @migrator.create_model
    class UserProperty(BaseModel):
        user = peewee.ForeignKeyField(User)
        module = peewee.TextField(null=False)
        key = peewee.TextField(null=False)
        value = peewee.TextField(null=False)

    class BaseDocumentModel(peewee.Model):
        created = peewee.DateTimeField(null=False, default=datetime.now, formats=["%s"])
        edited = peewee.DateTimeField(null=False, default=datetime.now, index=True, formats=["%s"])
        is_deleted = peewee.BooleanField(null=False, default=False)
        owner = peewee.ForeignKeyField(User, null=True)

    # Tagging
    @migrator.create_model
    class Tag(BaseModel):
        tag = peewee.TextField(null=False)
        owner = peewee.ForeignKeyField(User)

    @migrator.create_model
    class FuzzyTag(BaseModel):
        tag = peewee.ForeignKeyField(Tag)
        fuzzy = peewee.TextField(null=False)

    # Category
    @migrator.create_model
    class Category(BaseDocumentModel):
        name = peewee.TextField()
        comment = peewee.TextField(default="")
        is_archived = peewee.BooleanField(default=False)
        is_protected = peewee.BooleanField(default=False)
        order = peewee.IntegerField(default=0)
        path = peewee.TextField()
        parent = peewee.ForeignKeyField("self", backref="children", null=True)

    # Notes
    @migrator.create_model
    class Note(BaseDocumentModel):
        title = peewee.TextField()
        content = peewee.TextField()
        is_archived = peewee.BooleanField(default=False)
        is_pinned = peewee.BooleanField(default=False)
        tags = peewee.ManyToManyField(Tag)
        category = peewee.ForeignKeyField(Category, null=True, default=None, backref="notes")
        due_date = peewee.DateTimeField(null=True, default=None, )

    migrator.create_model(Note.tags.through_model)

    # Task
    @migrator.create_model
    class Task(BaseDocumentModel):
        title = peewee.TextField()
        is_completed = peewee.BooleanField(default=False)
        is_archived = peewee.BooleanField(default=False)
        note = peewee.ForeignKeyField(Note, null=True, backref="tasks")
        category = peewee.ForeignKeyField(Category, null=True, backref="tasks")
        due_date = peewee.DateTimeField(null=True, default=None, formats=["%s"])
        color = peewee.IntegerField(null=False, default=0)
        order = peewee.IntegerField(null=False, default=0)

    pass


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
    pass
