from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID

from app.db.model import Inventory

class InventoryService:
    async def get_all_inventory(self,session: AsyncSession):
        statement = select(Inventory).order_by(desc(Inventory.last_update))
        results = await session.exec(statement)
        inventory = results.all()
        return inventory

    async def get_inventory_item(self, inventory_id: str, session: AsyncSession):
        inventory_uuid = UUID(inventory_id)
        statement = select(Inventory).where(Inventory.id == inventory_uuid)
        results = await session.exec(statement)
        inventory_item = results.first()
        return inventory_item
