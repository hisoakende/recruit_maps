import uuid

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.db_schemas import Base


class DbUser(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    @hybrid_property
    def email(self) -> str:
        return self.username

    @property
    def is_active(self) -> bool:
        return True
