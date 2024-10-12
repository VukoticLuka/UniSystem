from typing import List

from fastapi import APIRouter

from app.core.session import get_async_session
from app.models.schemas.student_schema import DbStudent, StudentDisplay, StudentUpdate
from app.models.student import Student

from app.core.services import handle_result

router = APIRouter(
    prefix='/student',
    tags=['student']
)


@router.post("/", status_code=201)
async def create(student: DbStudent, session: get_async_session):
    from app.api.Student.utils import creation
    async with session.begin():
        return await creation(Student(**student.model_dump()), session)


@router.get("/", response_model=List[StudentDisplay])
async def get_all_student(session: get_async_session):
    from app.api.Student.utils import get_all
    async with session.begin():
        return await get_all(session)


@router.get("/{username}", response_model=StudentDisplay)
async def get_student(username: str, session: get_async_session):
    from app.api.Student.utils import get_student
    async with session.begin():
        return await handle_result(get_student, username, session)


# @router.get("/")
# async def get_by_idx(idx: int, session: get_async_session):
#     async with session.begin():
#         result = await session.execute(select(student).where(student.id == idx))
#         student = result.scalar_one_or_none()
#         if not student:
#             raise HTTPException(status_code=404,
#                                 detail="student not found")
#
#     return student


@router.patch("/{username}", response_model=StudentDisplay)
async def update(username: str, update_dict: StudentUpdate, session: get_async_session):
    from app.api.Student.utils import student_update
    async with session.begin():
        return await handle_result(student_update, username, session, update_dict)


@router.delete("/{username}", response_model=StudentDisplay)
async def delete(username: str, session: get_async_session):
    from app.api.Student.utils import delete_student
    async with session.begin():
        return await handle_result(delete_student, username, session)
