from typing import AsyncIterator, Dict

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.base import Base
from app.core.config import settings
from app.core.session import async_engine
from app.api.Student import endpoints as student
from app.api.Course import endpoints as course
from app.api.StudCourse import endpoints as stud_course


def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        # oslobadjanje resursa

    app = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
    )
    app.include_router(router=student.router)
    app.include_router(router=course.router)
    app.include_router(router=stud_course.router)

    @app.get("/")
    async def check_health() -> Dict[str, str]:
        return {"msg": "Ok"}

    # app.middleware(
    #     CORSMiddleware(
    #     allow_origins=settings.CORS,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"]
    #     )
    # )

    return app


app = create_app()
