from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db_session
from src.tags.repositories import TagRepository
from src.tags.services import TagService


def get_tag_repository(
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> TagRepository:
    return TagRepository(db_session)


def get_tag_services(
        tag_repository: Annotated[TagRepository, Depends(get_tag_repository)]
) -> TagService:
    return TagService(tag_repository)
