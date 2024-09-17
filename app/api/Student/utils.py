from typing import Optional, Dict

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.student_schema import StudentDisplay, StudentUpdate
from app.models.student_model import Student


async def creation(student: Student, session: AsyncSession) -> Dict:
    student_check = await get(student.username, session)
    if student_check is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Student with username={student.username} already exists")
    session.add(student)
    return {"msg": f"New student {student.username} successfully created"}


async def get(username: str, session: AsyncSession) -> Optional[StudentDisplay]:
    stmt = select(Student).where(Student.username == username)
    result = await session.execute(stmt)
    student = result.scalar()
    if student is None:
        return None
    return StudentDisplay.model_validate(student)


async def student_update(username: str,
                         update_dict: StudentUpdate,
                         session: AsyncSession) -> StudentDisplay:
    student = await get(username, session)
    if student is None:
        raise HTTPException(status_code=404,
                            detail="Student not found")
    result = await session.execute(update(Student).
                                   where(Student.username == username).
                                   values(**update_dict.model_dump(exclude_unset=True, exclude_none=True)))
    ####ovde imas gresku gde kao da ne moze da se vrati taj student koji je update
    updated_student = result.scalar_one()

    return StudentDisplay.model_validate(updated_student)
