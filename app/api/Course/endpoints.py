from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.services import handle_result
from app.models.schemas.course_schema import DbCourse, CourseDisplay
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
        return await handle_result(course_fetching,name,session)
