import logging
from typing import AsyncIterator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .config import settings, AppStage

logger = logging.getLogger(__name__)

db_url = settings.TEST_DB_URI if settings.DEV_STAGE == "develop" else settings.PRODUCTION_DB

async_engine = create_async_engine(
    url=db_url,
    pool_pre_ping=True,
    future=True,
    # pool_size=settings.DB_POOL_SIZE,
    # max_overflow=settings.MAX_OVERFLOW,
    connect_args={'check_same_thread': False},
    # echo for test purpose
    echo=True
)

async_session = async_sessionmaker(bind=async_engine, autoflush=False,
                                   autocommit=False,
                                   expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session

get_async_session = Annotated[AsyncSession, Depends(get_session)]
