from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any
from uuid import UUID

async def check_fk_exists(
    model: Any,
    id_value: UUID,
    field_name: str,
    session: AsyncSession,
):
    ojb = await session.get(model, id_value)

    if ojb is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{field_name} not found")

    return ojb
