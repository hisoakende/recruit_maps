from typing import Annotated

from fastapi import UploadFile, Form, File
from pydantic import BaseModel


class TagCreate(BaseModel):
    latitude: float
    longitude: float
    description: str
    image: UploadFile | None = None

    @classmethod
    def as_form(
            cls,
            latitude: Annotated[float, Form()],
            longitude: Annotated[float, Form()],
            description: Annotated[str, Form()],
            image: Annotated[UploadFile, File()] = None
    ) -> 'TagCreate':
        return cls(
            latitude=latitude,
            longitude=longitude,
            description=description,
            image=image
        )
