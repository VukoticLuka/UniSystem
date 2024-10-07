from typing import Optional, Dict, Callable

from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.student_schema import StudentDisplay, StudentUpdate
from app.models.student_model import Student


async def creation(student: Student, session: AsyncSession) -> Dict:
    student_check = await get_student(student.username, session)
    if student_check is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Student with username={student.username} already exists")
    session.add(student)
    return {"msg": f"New student {student.username} successfully created"}


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
        raise HTTPException(status_code=404,
                            detail="Student not found")
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

async def handle_result(func: Callable[[str, AsyncSession], Optional[StudentDisplay]],
                        username: str,
                        session: AsyncSession,
                        update_dict: Optional[StudentUpdate] = None) -> StudentDisplay:

    if update_dict is not None:
        student = await func(username, update_dict, session)
    else:
        student = await func(username, session)

    if not student:
        raise HTTPException(status_code=404,
                            detail=f"Student {username} not found")
    return student
