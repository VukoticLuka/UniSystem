from sqlalchemy import Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base
from enum import Enum


class Level(Enum):
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORAL = "doctoral"


class Student(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, index=True, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    firstname: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    level: Mapped[Level] = mapped_column(SqlEnum(Level))
