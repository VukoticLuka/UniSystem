from typing import Optional, Dict, Callable, List

from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.student_schema import StudentDisplay, StudentUpdate
from app.models.student import Student
from app.core.custom_exceptions import EntityNotFound, EntityAlreadyExists


async def creation(student: Student, session: AsyncSession) -> Dict:
    student_check = await get_student(student.username, session)
    if student_check is not None:
        raise EntityAlreadyExists(Student, student.username)
    session.add(student)
    return {"msg": f"New student {student.username} successfully created"}


async def get_all(session: AsyncSession) -> List[StudentDisplay]:
    stmt = select(Student)
    result = await session.execute(stmt)

    students = result.scalars().all()

    return [StudentDisplay.model_validate(student) for student in students]


async def get_student(username: str, session: AsyncSession) -> Optional[StudentDisplay]:
    stmt = select(Student).where(Student.username == username)
    result = await session.execute(stmt)
    student = result.scalar()
    if student is None:
        return None
    return StudentDisplay.model_validate(student)


async def student_update(username: str,
                         update_dict: StudentUpdate,
                         session: AsyncSession) -> StudentDisplay:
    student = await get_student(username, session)
    if student is None:
        raise EntityNotFound(Student, username)
    await session.execute(update(Student).
                          where(Student.username == username).
                          values(**update_dict.model_dump(exclude_unset=True, exclude_none=True)))

    updated_student = await get_student(username=username, session=session)

    return updated_student


async def delete_student(username: str, session: AsyncSession) -> Optional[StudentDisplay]:
    student = await get_student(username, session)
    if not student:
        return student
    await session.execute(delete(Student).where(Student.username == username))

    return StudentDisplay.model_validate(student)


