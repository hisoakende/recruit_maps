import random
import string
import uuid

from fastapi import UploadFile

from src import config
from src.tags.exceptions import TagDoesntExist, NotPermitted
from src.tags.filters import TagFilters
from src.tags.models import Tag
from src.tags.repositories import TagRepository
from src.tags.schemas import TagCreate
from src.users.models import User


class TagService:

    def __init__(self, repository: TagRepository) -> None:
        self._repository = repository

    async def get_tags(self, user: User | None, tag_filters: TagFilters) -> list[Tag]:
        user_id = user.id if User is not None else None
        return await self._repository.get_tags(user_id, tag_filters)

    async def create_tag(self, user: User | None, tag_create: TagCreate) -> Tag:
        if tag_create.image is not None:
            image_path = _save_image(tag_create.image)
        else:
            image_path = None

        tag = Tag(
            latitude=tag_create.latitude,
            longitude=tag_create.longitude,
            description=tag_create.description,
            image=image_path,
            likes=0,
            is_liked=False,
            user=user
        )

        await self._repository.create_tag(tag)
        return tag

    async def delete_tag(self, user: User | None, tag_id: uuid.UUID) -> None:
        if user is None:
            raise NotPermitted

        tag = await self._get_tag(user, tag_id)
        if tag.user is None or tag.user.id != user.id:
            raise NotPermitted

        await self._repository.delete_tag(tag_id)

    async def like_tag(self, user: User | None, tag_id: uuid.UUID) -> Tag:
        if user is None:
            raise NotPermitted

        tag = await self._get_tag(user, tag_id)
        tag.like()
        await self._repository.create_like(user.id, tag_id)

        return tag

    async def delete_like_from_tag(self, user: User | None, tag_id: uuid.UUID) -> None:
        if user is None:
            raise NotPermitted

        tag = await self._get_tag(user, tag_id)
        tag.delete_like()
        await self._repository.delete_like_from_tag(user.id, tag_id)

    async def _get_tag(self, user: User, tag_id: uuid.UUID) -> Tag:
        tag = await self._repository.get_tag(user.id, tag_id)
        if tag is None:
            raise TagDoesntExist
        return tag


def _save_image(file: UploadFile) -> str:
    filename = _create_filename(file.filename)
    with open(f'{config.STORAGE_PATH}/{filename}', 'wb') as disc_file:
        disc_file.write(file.file.read())
    return f'/{config.STORAGE_PATH}/{filename}'


def _create_filename(file_name: str) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(10)) + '_' + file_name
