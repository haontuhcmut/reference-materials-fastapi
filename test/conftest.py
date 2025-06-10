from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from app.main import app
from app.db.session import get_session
from fastapi.testclient import TestClient
import pytest

from app.config import Config

testing_engine = create_async_engine(Config.TESTING_DATABASE_URL)

AsyncSessionLocal = sessionmaker(testing_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
async def test_client():
    async with testing_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    #override the session
    app.dependency_overrides[get_session] = test_client

    with TestClient(app) as client:
        yield client