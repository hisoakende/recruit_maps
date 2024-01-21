import uuid

from fastapi_users import BaseUserManager, UUIDIDMixin

from src import config
from src.users.db_schemas import DbUser


class UserManager(UUIDIDMixin, BaseUserManager[DbUser, uuid.UUID]):
    reset_password_token_secret = config.JWT_SECRET
    verification_token_secret = config.JWT_SECRET
