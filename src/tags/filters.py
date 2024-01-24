from typing import Union

from fastapi import Query
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo
from sqlalchemy import Select, text

from src.filters import BaseFilter
from src.tags.db_schemas import DbTag
from src.users.db_schemas import DbUser
from src.users.filters import UserFilter


class TagFilters(BaseFilter):
    image: str | None = None
    image__neq: str | None = None
    order_by: list[str] = None
    user: UserFilter | None = FilterDepends(with_prefix('user', UserFilter))

    class Constants(BaseFilter.Constants):
        model = DbTag

    @field_validator('image', 'image__neq', mode='before')
    def process_image(cls, value: str) -> str | None:
        if value in ('none', 'null'):
            return None

        return value

    def sort(self, query: Union[Query, Select]):
        if not self.ordering_values:
            return query

        for field_name in self.ordering_values:
            direction = Filter.Direction.asc
            if field_name.startswith('-'):
                direction = Filter.Direction.desc
            field_name = field_name.replace('-', '').replace('+', '')

            if field_name.startswith('user'):
                model = DbUser
                field_name = field_name.split('__')[-1]
            else:
                model = self.Constants.model

            try:
                order_by_field = getattr(model, field_name)
                query = query.order_by(getattr(order_by_field, direction)())

            except AttributeError:
                direction = ' ASC' if direction == Filter.Direction.asc else ' DESC'
                query = query.order_by(text(field_name + direction))

        return query

    @field_validator('order_by')
    def validate_order_by(cls, value, field: ValidationInfo):
        if value is None:
            return None

        allowed_field_names = ['description', 'user__username', 'likes', 'is_liked']

        for field_name in value:
            field_name = field_name.replace('+', '').replace('-', '')
            if field_name not in allowed_field_names:
                raise ValueError(f'You may only sort by: {", ".join(allowed_field_names)}')

        return value
