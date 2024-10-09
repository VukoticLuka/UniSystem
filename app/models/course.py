from sqlalchemy import Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base
from enum import Enum


class Semester(Enum):
    FIRST = "first"
    SECOND = "second"


class Course(Base):
    __tablename__ = "courses"
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    espb: Mapped[int] = mapped_column(Integer, nullable=False)
    semester: Mapped[Semester] = mapped_column(SqlEnum(Semester), nullable=False)
    study_year: Mapped[int] = mapped_column(Integer, nullable=False)

    #add students_ids column