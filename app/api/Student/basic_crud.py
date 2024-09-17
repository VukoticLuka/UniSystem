from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.core.session import get_async_session
from app.models.schemas.student_schema import DbStudent, StudentDisplay, StudentUpdate
from app.models.student_model import Student

router = APIRouter(
    prefix='/student',
    tags=['student']
)


@router.post("/")
async def create(student: DbStudent, session: get_async_session):
    from app.api.Student.utils import creation
    async with session.begin():
        return await creation(Student(**student.model_dump()), session)


@router.get("/{username}", response_model=StudentDisplay)
async def get_student(username: str, session: get_async_session):
    from app.api.Student.utils import get
    async with session.begin():
        return await get(username, session)


@router.get("/")
async def get_by_idx(idx: int, session: get_async_session):
    async with session.begin():
        result = await session.execute(select(Student).where(Student.id == idx))
        student = result.scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404,
                                detail="Student not found")

    return student


# @router.patch("/{username}", response_model=StudentDisplay)
# async def update(username: str, update_dict: StudentUpdate, session: get_async_session):
#     from app.api.Student.utils import student_update
#     async with session.begin():
#         return await student_update(username, update_dict, session)
