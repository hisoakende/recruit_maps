import uuid
from typing import Any

from fastapi.exceptions import RequestValidationError
from pydantic import field_validator

from src.filters import BaseFilter
from src.users.db_schemas import DbUser


class UserFilter(BaseFilter):
    id: uuid.UUID | str | None = None
    username: str | None = None

    class Constants(BaseFilter.Constants):
        model = DbUser

    @field_validator('id', mode='before')
    def process_user(cls, value: Any) -> uuid.UUID | str | None:
        if value in ('none', 'null'):
            return None

        if isinstance(value, uuid.UUID):
            return value

        try:
            return uuid.UUID(value, version=4)
        except ValueError:
            raise RequestValidationError('Field user must be uuid')
