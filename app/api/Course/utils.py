from typing import Optional, Callable, List
from fastapi.responses import JSONResponse
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.custom_exceptions import EntityAlreadyExists, EntityNotFound
from app.models.course import Course
from app.models.schemas.course_schema import DbCourse, CourseDisplay, CourseUpdate


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


async def delete_course_by_name(name: str, session: AsyncSession) -> Optional[CourseDisplay]:
    course = await course_fetching(name, session)

    if not course:
        return None

    result = await session.execute(delete(Course).where(Course.name == name))

    if result.rowcount != 1:
        raise Exception(f"None or multiple row was deleted on course name {name}")

    return CourseDisplay.model_validate(course)


async def update_course_by_name(name: str,
                                update_dict: CourseUpdate,
                                session: AsyncSession) -> Optional[CourseDisplay]:
    result = await course_fetching(name, session)

    if result is None:
        return result

    await session.execute(update(Course)
                          .where(Course.name == name)
                          .values(**update_dict.model_dump(exclude_unset=True, exclude_none=True)))

    return await course_fetching(name,session)
