import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

logger = logging.getLogger(__name__)

async_engine = create_async_engine(
    url=settings.TEST_DB_URI,
    pool_pre_ping=True,
    future=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    connect_args={'check_same_thread': False}
)

async_session = async_sessionmaker(bind=async_engine, autoflush=False, autocommit=False, expire_on_commit=False)
