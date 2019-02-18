import peewee

# import logging

import json, random
import jwt, bcrypt
import datetime
import app
from app import components


from app.user.model import User, Role, Token


class TestUtils:

    post_args = {
        "content_type": "application/json"
    }

    ADMIN_ROLE = "ADMIN"
    ADMIN_USER = "admin"
    ADMIN_PW = "admin"

    REGULAR_USER = "user"
    REGULAR_PW = "password"

    REGULAR_ALT_USER = "user2"
    REGULAR_ALT_PW = "password2"

    INACTIVE_USER = "inactive-user"
    INACTIVE_PW = "password"

    def __init__(self):
        self._users = {}
        pass

    def _setup_app(self):
        self._db = peewee.SqliteDatabase(":memory:")
        components.DB.initialize(self._db)
        components.DB.connect()
        components.DB.create_tables(app.MODELS, safe=True)
        self.config = app.APP.config
        self.app = app.APP.test_client()
        self._create_test_users()

    def _create_test_users(self):
        # admin user and role
        admin_role = Role(name=self.ADMIN_ROLE)
        admin_role.save()

        admin_user = User(
            name=self.ADMIN_USER,
            password=self.encode_password(self.ADMIN_PW),
            is_active=True,
            user_id=self._user_gen_id()
        )
        admin_user.save()
        admin_user.permissions.add(admin_role)
        # admin_user.save()

        self._users[self.ADMIN_USER] = admin_user

        # regular user
        regular_user = User(
            name=self.REGULAR_USER,
            password=self.encode_password(self.REGULAR_PW),
            is_active=True,
            user_id=self._user_gen_id()

        )
        regular_user.save()

        self._users[self.REGULAR_USER] = regular_user

        # regular secondary user
        regular_user = User(
            name=self.REGULAR_ALT_USER,
            password=self.encode_password(self.REGULAR_ALT_PW),
            is_active=True,
            user_id=self._user_gen_id()
        )
        regular_user.save()

        self._users[self.REGULAR_ALT_USER] = regular_user

        # inactive user
        inactive_user = User(
            name=self.INACTIVE_USER,
            password=self.encode_password(self.INACTIVE_PW),
            is_active=False,
            user_id=self._user_gen_id()

        )
        inactive_user.save()

        self._users[self.INACTIVE_USER] = inactive_user

        pass

    def response(self, response, code=200):
        self.assertIsNotNone(response)
        self.assertEqual(code, response.status_code)
        response_json = json.loads(response.data)
        return response_json

    def encode_password(self, password):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            self.config["SECRET_KEY"]
        ).decode()

        return password

    def create_user_token(self, username):
        if not self._users:
            self._create_test_users()
        if username not in self._users:
            return {}
        token = self._gentoken(self._users[username])
        return "Bearer %s" % token
        pass

    def create_user_header(self, username):
        return {"headers": {"Authorization": self.create_user_token(username)}}

    def _user_gen_id(self):
        return "".join(random.choice("1234567890qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ") for _ in range(32))

    def _gentoken(self, user):
        token = Token(
            payload=self._encode_jwt(user.user_id),
            user=user
        )
        token.save()
        return token.token_id

    def _encode_jwt(self, user_id):
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=9999),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
                "cid": "Testing"  # Client id / identifier (ip, agent, etc ... )
            }
            return jwt.encode(
                payload,
                self.config["SECRET_KEY"],
                algorithm="HS256"
            )
        except Exception as e:
            return e
