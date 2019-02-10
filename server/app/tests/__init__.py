import peewee

import app
import json
from app import components

from app.user.model import User, Role


class TestUtils:

    post_args = {
        "content_type": "application/json"
    }

    ADMIN_ROLE = "ADMIN"
    ADMIN_USER = "admin"
    ADMIN_PW = "admin"

    REGULAR_USER = "user"
    REGULAR_PW = "password"

    INACTIVE_USER = "user"
    INACTIVE_PW = "password"

    def __init__(self):
        pass

    def _setup_app(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.MODELS, safe=True)
        self.app = app.APP.test_client()
        self._crete_test_users()

    def _create_test_users(self):
        # amdin user and role
        admin_role = Role(name=self.ADMIN_ROLE)
        admin_role.save()

        admin_user = User(
            name=self.ADMIN_USER,
            password=self._encode_password(self.ADMIN_PW),
            is_active=True
        )
        admin_user.save()

        admin_user.permissions.add(admin_role)
        admin_user.save()

        # regular user
        regular_user = User(
            name=self.REGULAR_USER,
            password=self._encode_password(self.REGULAR_PW),
            is_active=True
        )
        regular_user.save()

        # inactive user
        inactive_user = User(
            name=self.INACTIVE_USER,
            password=self._encode_password(self.INACTIVE_PW),
            is_active=False
        )
        inactive_user.save()

        pass

    def _response(self, response, code=200):
        self.assertEqual(code, response.status_code)
        response_json = json.loads(response.data)
        return response_json

    def _encode_password(self, password):
        # TODO bcrypt something goez here
        # assert "SECRET_KEY" in self.app.config
        # secret = self.app.config["SECRET_KEY"]
        return password
