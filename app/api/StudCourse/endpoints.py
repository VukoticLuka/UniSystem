from fastapi import APIRouter
from sqlalchemy import select
from app.core.session import get_async_session
from app.models.course import Course
from app.models.student import Student
from app.core.custom_exceptions import EntityNotFound

router = APIRouter(
    prefix="/student-course",
    tags=["student-course"]
)


@router.post("/{username}-{course_name}")
async def enroll_stud_to_course(username: str,
                                course_name: str,
                                session: get_async_session):
    async with session.begin():
        stud_db = await session.execute(select(Student).where(Student.username == username))
        student = stud_db.scalar_one_or_none()

        course_db = await session.execute(select(Course).where(Course.name == course_name))
        course = course_db.scalar_one_or_none()

        if not student:
            raise EntityNotFound(Student, username)
        if not course:
            raise EntityNotFound(Course, course_name)

        student.courses.add(course)
    await session.commit()

    return {"msg": "Ok"}
