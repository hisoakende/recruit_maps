import uuid

from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import ConfigDict, field_validator


class UserRead(CreateUpdateDictModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str


class UserCreate(CreateUpdateDictModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        if not password:
            raise ValueError('Password must not be empty')
        return password

    @property
    def email(self) -> str:
        return self.username
