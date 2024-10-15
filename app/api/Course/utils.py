from typing import Optional, Callable, List
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.custom_exceptions import EntityAlreadyExists, EntityNotFound
from app.models.course import Course
from app.models.schemas.course_schema import DbCourse, CourseDisplay


async def course_creation(course: DbCourse, session: AsyncSession) -> JSONResponse:
    existence_check = await course_fetching(course.name, session)

    if existence_check is not None:
        raise EntityAlreadyExists(Course, course.name)

    new_course = Course(**course.model_dump())
    session.add(new_course)
    return JSONResponse({"msg": f"New course {course.name} has been created"})


async def course_fetching(name: str, session: AsyncSession) -> Optional[CourseDisplay]:
    stmt = select(Course).where(Course.name == name)
    result = await session.execute(stmt)

    course = result.scalars().first()
    if course is None:
        return None
    return CourseDisplay.model_validate(course)


async def all_courses(session: AsyncSession) -> List[CourseDisplay]:
    result = await session.execute(select(Course))

    courses = result.scalars().all()

    return [CourseDisplay.model_validate(course) for course in courses] if courses else []
