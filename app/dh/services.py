import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import Dh
from sqlmodel import desc, select
from app.dh.schemas import CreateDhScheme

class DhServices:
    async def get_dh(self, session: AsyncSession):
        statement = select(Dh).order_by(desc(Dh.code))
        results = await session.exec(statement)
        dh = results.all()
        return dh

    async def get_dh_item(self, dh_id: str, session: AsyncSession):
        dh_uuid = uuid.UUID(dh_id)
        statement = select(Dh).where(Dh.id == dh_uuid)
        result = await session.exec(statement)
        dh = result.first()
        return dh

    async def create_dh(self, dh_data: CreateDhScheme, session: AsyncSession):
        dh_data_dict = dh_data.model_dump()
        new_dh = Dh(**dh_data_dict)
        session.add(new_dh)
        await session.commit()
        return new_dh

    async def update_dh(self, dh_id: str, data_update: CreateDhScheme, session: AsyncSession):
        dh_to_update = await self.get_dh_item(dh_id, session)
        if dh_to_update is not None:
            update_data_dict = data_update.model_dump()
            for key, value in update_data_dict.items():
                setattr(dh_to_update, key, value)
                await session.commit()
                return dh_to_update
        else:
            return None

    async def delete_dh(self, dh_id: str, session: AsyncSession):
        dh_to_delete = await self.get_dh_item(dh_id, session)
        if dh_to_delete is not None:
            await session.delete(dh_to_delete)
            await session.commit()
            return dh_to_delete
        else:
            return None
