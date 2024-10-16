from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.session import get_async_session
from app.models.course import Course
from app.models.student import Student
from app.core.custom_exceptions import EntityNotFound

router = APIRouter(
    prefix="/student-course",
    tags=["student-course"]
)


@router.post("/{username}-{course_name}")
async def enroll_stud_to_course(username: str,
                                course_name: str,
                                session: get_async_session):
    async with session.begin():
        stud_db = await session.execute(select(Student).where(Student.username == username))
        student = stud_db.scalar_one_or_none()

        course_db = await session.execute(select(Course).where(Course.name == course_name))
        course = course_db.scalar_one_or_none()

        if not student:
            raise EntityNotFound(Student, username)
        if not course:
            raise EntityNotFound(Course, course_name)

        student.courses.add(course)
    await session.commit()

    return {"msg": f"Student {username} successfully enrolled in the {course_name} course"}


@router.get('/by-student/{username}')
async def get_all_student_courses(username: str, session: get_async_session):
    async with session.begin():
        result = await session.execute(
            select(Course.course_id, Course.name, Course.espb).
            join(Student.courses).
            where(Student.username == username)
        )

        courses = result.all()

        course_list = [
            {"course_id": course_id, "name": name, "espb": espb}
            for course_id, name, espb in courses
        ]

        return course_list


@router.get('/course/{course_name}')
async def get_all_students_on_course(course_name: str, session: get_async_session):
    async with session.begin():
        result = await session.execute(
            select(Student.username).
            join(Course.students).
            where(Course.name == course_name)
        )

        return result.scalars().all()


@router.get('/grade/{stud_name}-{course_name}')
async def get_grade(stud_id: int, course_id: int, session: get_async_session):
    from app.models.stud_course import student_course
    async with session.begin():
        result_db = await session.execute(
            student_course.select()
            .where(student_course.c.student_id == stud_id)
            .where(student_course.c.course_id == course_id)
        )

        result = result_db.fetchone()

        return result.grade


@router.post("/grade/{stud_id}-{course_id}")
async def insert_stud_grade(stud_id: int,
                            course_id: int,
                            grade: int,
                            session: get_async_session):
    from app.models.stud_course import student_course
    try:
        async with session.begin():
            await session.execute(
                student_course.update()
                .where(student_course.c.student_id == stud_id)
                .where(student_course.c.course_id == course_id)
                .values(grade=grade)
            )

        await session.commit()

        return JSONResponse({"msg": f"Grade {grade} added for student {stud_id} on course {course_id}."})
    except IntegrityError as e:
        raise HTTPException(status_code=400,
                            detail="Grade must be between 6 and 10")