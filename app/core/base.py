from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


ModelGen = TypeVar("ModelGen", bound=Base)
