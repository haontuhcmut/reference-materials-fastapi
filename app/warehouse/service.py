from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.db.model import Warehouse
from app.warehouse.schema import CreateWarehouseModel

class WarehouseService:
    async def get_all_warehouse(self, session: AsyncSession):
        statement = select(Warehouse).order_by(Warehouse.name)
        results = await session.exec(statement)
        warehouse = results.all()
        return warehouse

    async def get_warehouse_item(self, warehouse_id: str, session: AsyncSession):
        warehouse_uuid = UUID(warehouse_id)
        statement = select(Warehouse).where(Warehouse.id == warehouse_uuid)
        result = await session.exec(statement)
        warehouse = result.first()
        return warehouse

    async def create_warehouse(self, warehouse_data: CreateWarehouseModel, session: AsyncSession):
        data_dict = warehouse_data.model_dump()
        new_warehouse = Warehouse(**data_dict)
        session.add(new_warehouse)
        await session.commit()
        return new_warehouse

    async def update_warehouse(self, warehouse_id: str, update_data: CreateWarehouseModel, session: AsyncSession):
        update_to_warehouse = await self.get_warehouse_item(warehouse_id, session)
        if update_to_warehouse is not None:
            data_dict = update_data.model_dump()
            for key, value in data_dict.items():
                setattr(update_to_warehouse, key, value)
            await session.commit()
            return update_to_warehouse
        return None

    async def delete_warehouse(self, warehouse_id: str, session: AsyncSession):
        delete_to_warehouse = await self.get_warehouse_item(warehouse_id, session)
        if delete_to_warehouse is not None:
            await session.delete(delete_to_warehouse)
            await session.commit()
            return delete_to_warehouse
        return None
