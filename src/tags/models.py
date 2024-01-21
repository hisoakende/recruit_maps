import uuid

from pydantic import BaseModel, Field

from src.tags.exceptions import TagAlreadyIsLiked, TagIsNotLiked
from src.users.models import User


class Tag(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    latitude: float
    longitude: float
    description: str
    image: str | None
    likes: int
    is_liked: bool = False
    user: User | None

    def like(self) -> None:
        if self.is_liked:
            raise TagAlreadyIsLiked

        self.likes += 1
        self.is_liked = True

    def delete_like(self) -> None:
        if not self.is_liked:
            raise TagIsNotLiked

        self.likes -= 1
        self.is_liked = False
