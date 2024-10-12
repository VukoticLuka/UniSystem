from typing import Union

from sqlalchemy import Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base
from enum import Enum


class Level(str, Enum):
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORAL = "doctoral"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Student(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, index=True, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    firstname: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    index_number: Mapped[int] = mapped_column(Integer)
    enrollment_year: Mapped[int] = mapped_column(Integer)
    gender: Mapped[Union[Gender, None]] = mapped_column(SqlEnum(Gender), nullable=True)
    education: Mapped[Union[Level, None]] = mapped_column(SqlEnum(Level), nullable=True)
