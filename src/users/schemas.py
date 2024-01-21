import uuid

from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import ConfigDict


class UserRead(CreateUpdateDictModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str


class UserCreate(CreateUpdateDictModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str

    @property
    def email(self) -> str:
        return self.username
