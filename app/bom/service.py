from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.model import BillOfMaterial
from app.bom.schema import CreateBomModel

class BomService:
    async def get_all_bom(self, session: AsyncSession):
        statement = select(BillOfMaterial)
        results = await session.exec(statement)
        bom = results.all()
        return bom

    async def get_bom_item(self, bom_id: str, session: AsyncSession):
        bom_uuid = UUID(bom_id)
        statement = select(BillOfMaterial).where(BillOfMaterial.id == bom_uuid)
        result = await session.exec(statement)
        bom = result.first()
        return bom

    async def create_bom_item(self, bom_data: CreateBomModel, session: AsyncSession):
        data_dict = bom_data.model_dump()
        new_bom = BillOfMaterial(**data_dict)
        session.add(new_bom)
        await session.commit()
        return new_bom

    async def update_bom(self, bom_id: str, data_update: CreateBomModel, session: AsyncSession):
        bom_to_update = await self.get_bom_item(bom_id, session)
        if bom_to_update is not None:
            data_dict = data_update.model_dump()
            for key, value in data_dict.items():
                setattr(bom_to_update, key, value)
            await session.commit()
            return bom_to_update
        return None

    async def delete_bom(self, bom_id: str, session: AsyncSession):
        bom_to_delete = await self.get_bom_item(bom_id, session)
        if bom_to_delete is not None:
            await session.delete(bom_to_delete)
            await session.commit()
            return bom_to_delete
        return None