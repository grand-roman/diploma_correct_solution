import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_database_url():
    if os.environ.get("ENV") == "test":
        return os.getenv("DATABASE_URL_TEST")
    elif os.environ.get("ENV") == "debug":
        return os.getenv("DATABASE_URL_DEBUG")
    else:
        return os.getenv("DATABASE_URL")


engine = create_async_engine(get_database_url(), echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
