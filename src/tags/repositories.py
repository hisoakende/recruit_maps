import uuid

from sqlalchemy import select, func, bindparam, Select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.tags.db_schemas import DbTag, DbLike
from src.tags.filters import TagFilters
from src.tags.models import Tag
from src.users.db_schemas import DbUser
from src.users.models import User


class TagRepository:

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def get_tag(self, user_id: uuid.UUID | None, tag_id: uuid.UUID | None) -> Tag | None:
        sql = self._get_all_tags_sql().filter(DbTag.id == tag_id)
        query_result = await self._db_session.execute(sql, {'user_id': user_id})
        db_tag = query_result.mappings().one_or_none()
        if db_tag is None:
            return None

        return Tag(
            id=db_tag['DbTag'].id,
            latitude=db_tag['DbTag'].latitude,
            longitude=db_tag['DbTag'].longitude,
            description=db_tag['DbTag'].description,
            image=db_tag['DbTag'].image,
            likes=db_tag['likes'],
            is_liked=db_tag['is_liked'],
            user=User(
                id=db_tag['DbUser'].id,
                username=db_tag['DbUser'].username
            ) if db_tag['DbUser'] is not None else None
        )

    async def get_tags(self, user_id: uuid.UUID | None, filters: TagFilters) -> list[Tag]:
        sql = filters.filter(filters.sort(self._get_all_tags_sql()))
        raw_tags = await self._db_session.execute(sql, {'user_id': user_id})

        return [
            Tag(
                id=data['DbTag'].id,
                latitude=data['DbTag'].latitude,
                longitude=data['DbTag'].longitude,
                description=data['DbTag'].description,
                image=data['DbTag'].image,
                likes=data['likes'],
                is_liked=data['is_liked'],
                user=User(
                    id=data['DbUser'].id,
                    username=data['DbUser'].username
                ) if data['DbUser'] is not None else None
            )
            for data in raw_tags.mappings().fetchall()
        ]

    async def create_tag(self, tag: Tag) -> None:
        db_tag = DbTag(
            id=tag.id,
            latitude=tag.latitude,
            longitude=tag.longitude,
            description=tag.description,
            image=tag.image,
            user=tag.user.id if tag.user is not None else None
        )

        self._db_session.add(db_tag)
        await self._db_session.commit()

    async def delete_tag(self, tag_id: uuid.UUID) -> None:
        sql = delete(DbTag).where(DbTag.id == tag_id)
        await self._db_session.execute(sql)
        await self._db_session.commit()

    async def create_like(self, user_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        db_like = DbLike(
            tag=tag_id,
            user=user_id
        )

        self._db_session.add(db_like)
        await self._db_session.commit()

    async def delete_like_from_tag(self, user_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        sql = delete(DbLike).where(DbLike.user == user_id, DbLike.tag == tag_id)
        await self._db_session.execute(sql)
        await self._db_session.commit()

    @staticmethod
    def _get_all_tags_sql() -> Select:
        likes = select(func.count(DbLike.id)).where(DbLike.tag == DbTag.id).label('likes')
        is_liked = (
            select(DbLike)
            .where(DbLike.user == bindparam('user_id'), DbLike.tag == DbTag.id)
            .exists()
            .label('is_liked')
        )

        return select(DbTag, DbUser, likes, is_liked).join(DbUser, isouter=True)
