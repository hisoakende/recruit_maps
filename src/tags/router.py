import uuid
from typing import Annotated

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from src.tags.filters import TagFilters

from src.tags.dependencies import get_tag_services
from src.tags.exceptions import NotPermitted, TagDoesntExist, TagAlreadyIsLiked, TagIsNotLiked
from src.tags.models import Tag
from src.tags.schemas import TagCreate
from src.tags.services import TagService
from src.users.dependencies import get_user
from src.users.models import User

tag_filters_dependence = Annotated[TagFilters, FilterDepends(TagFilters)]
tag_create_dependence = Annotated[TagCreate, Depends(TagCreate.as_form)]
tag_service_dependence = Annotated[TagService, Depends(get_tag_services)]
user_dependence = Annotated[User | None, Depends(get_user)]

router = APIRouter(
    prefix='/api/tags',
    tags=['tags']
)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_tags(
        tag_service: tag_service_dependence,
        tag_filters: tag_filters_dependence,
        user: user_dependence
) -> list[Tag]:
    return await tag_service.get_tags(user, tag_filters)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_tag(
        tag_create: tag_create_dependence,
        tag_service: tag_service_dependence,
        user: user_dependence
) -> Tag:
    tag = await tag_service.create_tag(
        user, tag_create
    )
    return tag


@router.delete('/{tag_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
        tag_id: uuid.UUID,
        tag_service: tag_service_dependence,
        user: user_dependence
) -> None:
    try:
        await tag_service.delete_tag(user, tag_id)

    except NotPermitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    except TagDoesntExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/{tag_id}/likes', status_code=status.HTTP_201_CREATED)
async def like_tag(
        tag_id: uuid.UUID,
        tag_service: tag_service_dependence,
        user: user_dependence
) -> Tag:
    try:
        return await tag_service.like_tag(user, tag_id)

    except NotPermitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    except TagDoesntExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except TagAlreadyIsLiked as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.__doc__
        )


@router.delete('/{tag_id}/likes', status_code=status.HTTP_204_NO_CONTENT)
async def delete_like_from_tag(
        tag_id: uuid.UUID,
        tag_service: tag_service_dependence,
        user: user_dependence
) -> None:
    try:
        await tag_service.delete_like_from_tag(user, tag_id)

    except NotPermitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    except TagDoesntExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except TagIsNotLiked as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.__doc__
        )
