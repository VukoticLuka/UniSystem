from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.services import handle_result
from app.models.schemas.course_schema import DbCourse, CourseDisplay, CourseUpdate
from app.core.session import get_async_session

router = APIRouter(
    prefix="/course",
    tags=["course"]
)


@router.post("/", response_class=JSONResponse)
async def create_course(course: DbCourse, session: get_async_session) -> JSONResponse:
    from app.api.Course.utils import course_creation

    async with session.begin():
        return await course_creation(course, session)


@router.get("/{name}", response_model=CourseDisplay)
async def get_course(name: str, session: get_async_session) -> CourseDisplay:
    from app.api.Course.utils import course_fetching

    async with session.begin():
        return await handle_result(course_fetching, name, session)


@router.get("/", response_model=List[CourseDisplay])
async def get_all_courses(session: get_async_session) -> List[CourseDisplay]:
    from app.api.Course.utils import all_courses

    async with session.begin():
        return await all_courses(session)


@router.delete("/{name}", status_code=200, response_model=CourseDisplay)
async def delete_course(name: str, session: get_async_session) -> CourseDisplay:
    from app.api.Course.utils import delete_course_by_name

    async with session.begin():
        return await handle_result(delete_course_by_name, name, session)


@router.patch("/{name}", status_code=200, response_model=CourseDisplay)
async def update_course(name: str,
                        update_dict: CourseUpdate,
                        session: get_async_session) -> CourseDisplay:
    from app.api.Course.utils import update_course_by_name

    async with session.begin():
        return await handle_result(update_course_by_name,name,session,update_dict)