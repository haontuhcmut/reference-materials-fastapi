from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.db.model import OrderItem
from app.order_item.schema import CreateOrderItemModel

class OrderItemService:
    async def get_all_order_item(self, session: AsyncSession):
        statement = select(OrderItem)
        results = await session.exec(statement)
        order_item = results.all()
        return order_item

    async def get_order_item(self, order_item_id: str, session:AsyncSession):
        order_item_uuid = UUID(order_item_id)
        statement = select(OrderItem).where(OrderItem.id == order_item_uuid)
        result = await session.exec(statement)
        order_item = result.first()
        return order_item

    async def create_order_item(self, order_item_data: CreateOrderItemModel, session: AsyncSession):
        data_dict = order_item_data.model_dump()
        new_order_item = OrderItem(**data_dict)
        session.add(new_order_item)
        await session.commit()
        return new_order_item

    async def update_order_item(self, order_item_id: str, update_data: CreateOrderItemModel, session: AsyncSession):
        order_item_to_update = await self.get_order_item(order_item_id, session)
        if order_item_to_update is not None:
            data_dict = update_data.model_dump()
            for key, value in data_dict.items():
                setattr(order_item_to_update, key, value)
            await session.commit()
            return order_item_to_update
        return None

    async def delete_order_item(self, order_item_id: str, session: AsyncSession):
        order_item_to_delete = await self.get_order_item(order_item_id, session)
        if order_item_to_delete is not None:
            await session.delete(order_item_to_delete)
            await session.commit()
            return order_item_to_delete
        return None












