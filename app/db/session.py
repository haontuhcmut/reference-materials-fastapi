from sqlmodel import SQLModel, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config import Config

database_url = Config.DATABASE_URL

engine = create_async_engine(url=database_url, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # ⚠️ Objects will NOT be automatically refreshed after commit!
)
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session