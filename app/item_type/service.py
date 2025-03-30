from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.model import ItemType
from app.item_type.schema import CreateItemTypeModel

class ItemTypeService:
    async def get_all_type(self, session: AsyncSession):
        statement = select(ItemType).order_by(ItemType.type_name)
        results = await session.exec(statement)
        item_type = results.all()
        return item_type

    async def get_type(self, type_id: str, session: AsyncSession):
        type_uuid = UUID(type_id)
        statement = select(ItemType).where(ItemType.id == type_uuid)
        result = await session.exec(statement)
        item_type = result.first()
        return item_type

    async def create_type(self, data_type: CreateItemTypeModel, session: AsyncSession):
        data_dict = data_type.model_dump()
        new_type = ItemType(**data_dict)
        session.add(new_type)
        await session.commit()
        return new_type

    async def update_type(self, type_id: str, data_update: CreateItemTypeModel, session: AsyncSession):
        update_to_type = await self.get_type(type_id, session)
        if update_to_type is not None:
            data_dict = data_update.model_dump()
            for key, value in data_dict.items():
                setattr(update_to_type, key, value)
            await session.commit()
            return update_to_type
        return None

    async def delete_type(self, type_id: str, session: AsyncSession):
        delete_to_type = await self.delete_type(type_id, session)
        if delete_to_type is not None:
            await session.delete(delete_to_type)
            await session.commit()
            return delete_to_type
        return None

