from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.db.session import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
