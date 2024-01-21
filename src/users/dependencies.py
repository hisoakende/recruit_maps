import uuid
from typing import Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db_session
from src.users.auth import auth_backend
from src.users.db_schemas import DbUser
from src.users.managers import UserManager
from src.users.models import User
from src.users.schemas import UserRead


def get_user_repository(
        session: Annotated[AsyncSession, Depends(get_db_session)]
) -> SQLAlchemyUserDatabase:
    return SQLAlchemyUserDatabase(session, DbUser)  # type: ignore


def get_user_manager(
        user_repository: Annotated[SQLAlchemyUserDatabase, Depends(get_user_repository)]
) -> UserManager:
    return UserManager(user_repository)


users_manager = FastAPIUsers[DbUser, uuid.UUID](get_user_manager, [auth_backend])


def get_user(
        user: Annotated[DbUser | None, Depends(users_manager.current_user(optional=True))]
) -> User:
    return User(
        id=user.id,
        username=user.username
    ) if user is not None else None
