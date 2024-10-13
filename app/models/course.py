from typing import List, Set

from sqlalchemy import Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base
from enum import Enum

from app.models.stud_course import student_course


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

    students: Mapped[Set['Student']] = relationship('Student',
                                                     secondary=student_course,
                                                     back_populates='courses',
                                                     lazy='selectin',
                                                     cascade='all')
