import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from app.config import Config
from fastapi_pagination import add_pagination

from app.db.session import get_session
from app.main import app

async_engine = create_async_engine(
    url=Config.TESTING_DATABASE_URL,
    poolclass=NullPool,
)

async_session = sessionmaker(
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
)


# Drop all tables after each test
@pytest_asyncio.fixture(scope="session")
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_db(async_db_engine):
    async with async_session() as session:
        await session.begin()

        yield session

        # Rollback any database changes made during the test to maintain test isolation
        await session.rollback()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_db):
    def override_get_db():
        yield async_db

    app.dependency_overrides[get_session] = override_get_db
    add_pagination(app)  # Pagination is registered
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")
