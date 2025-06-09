from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from sqlmodel import SQLModel
from app.main import app
from fastapi.testclient import TestClient
from app.db.session import get_session

import pytest_asyncio

from app.config import Config


#Create a session override the default db session
test_engine = create_async_engine(url=Config.TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)
async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with TestingSessionLocal() as session:
            yield session
    finally:
        await session.close()

@pytest_asyncio.fixture(scope="session")
async def test_client():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    app.dependency_overrides[get_session] = test_get_session

    with TestClient(app) as client:
        yield client







