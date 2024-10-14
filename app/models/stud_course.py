from sqlalchemy import Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


student_course = Table(
    "student_course",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.course_id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True)
)


