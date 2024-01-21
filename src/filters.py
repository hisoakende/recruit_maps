from fastapi_filter.contrib.sqlalchemy import Filter


class BaseFilter(Filter):

    @property
    def filtering_fields(self):
        fields = self.model_dump(exclude_unset=True)
        fields.pop(self.Constants.ordering_field_name, None)
        return fields.items()
