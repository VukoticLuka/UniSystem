from pydantic import BaseModel
from typing import TypeVar, Callable, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas.course_schema import CourseUpdate
from app.models.schemas.student_schema import StudentUpdate

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=Union[StudentUpdate, CourseUpdate])


async def handle_result(func: Callable[[str, AsyncSession], Optional[T]],
                        name: str,
                        session: AsyncSession,
                        update_dict: Optional[U] = None) -> T:
    from app.core.custom_exceptions import EntityNotFound

    if update_dict is not None:
        result = await func(name, update_dict, session)
    else:
        result = await func(name, session)

    if not result:
        raise EntityNotFound(T, name)
    return result
