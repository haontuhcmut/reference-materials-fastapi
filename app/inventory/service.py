from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID

from app.db.model import Inventory

class InventoryService:
    async def get_all_inventory(self, session:AsyncSession):
        statement = select(Inventory).order_by(desc(Inventory.last_update))
        results = await session.exec(statement)
        inventories = results.all()
        return inventories

    async def get_inventory_item(self, inventory_id: str, session: AsyncSession):
        inventory_uuid = UUID(inventory_id)
        statement = select(Inventory).where(Inventory.id == inventory_uuid)
        result = await session.exec(statement)
        inventory = result.first()
        return inventory

    async def get_inventory_by_product_id(self, product_id: str, session: AsyncSession):
        product_uuid = UUID(product_id)
        statement = select(Inventory).where(Inventory.product_id == product_uuid)
        result = await session.exec(statement)
        inventory = result.first()
        return inventory

    async def get_inventory_by_material_id(self, material_id: str, session: AsyncSession):
        material_uuid = UUID(material_id)
        statement = select(Inventory).where(Inventory.material_id == material_uuid)
        result = await session.exec(statement)
        inventory = result.first()
        return inventory
