from curses import echo

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings


async_engine = create_async_engine(
    url=settings.db_DSN,
    echo=False
)

async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=True)


class Base(DeclarativeBase):
    pass



