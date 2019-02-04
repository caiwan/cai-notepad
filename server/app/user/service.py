# coding=utf-8

from app import components
from app.user.model import User


class UserService(components.Service):
    name = "users"
    model_class = User

    def __init__(self):
        super().__init__()
