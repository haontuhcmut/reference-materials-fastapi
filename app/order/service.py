from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID

from app.db.model import Order
from app.order.schema import CreateOrderModel


class OrderService:
    async def get_all_order(self, session: AsyncSession):
        statement = select(Order).order_by(desc(Order.order_time))
        results = await session.exec(statement)
        order = results.all()
        return order

    async def get_order_item(self, order_id: str, session: AsyncSession):
        order_uuid = UUID(order_id)
        statement = select(Order).where(Order.id == order_uuid)
        result = await session.exec(statement)
        order = result.first()
        return order

    async def create_order(self, order_data: CreateOrderModel, session: AsyncSession):
        data_dict = order_data.model_dump()
        new_order = Order(**data_dict)
        session.add(new_order)
        await session.commit()
        return new_order

    async def update_order(self, order_id: str, update_data: CreateOrderModel, session: AsyncSession):
        order_to_update = await self.get_order_item(order_id, session)
        if order_to_update is not None:
            data_dict = update_data.model_dump()
            for key, value in data_dict.items():
                setattr(order_to_update, key, value)
            await session.commit()
            return order_to_update
        return None

    async def delete_order(self, order_id: str, session: AsyncSession):
        order_to_delete = await self.get_order_item(order_id, session)
        if order_to_delete is not None:
            await session.delete(order_to_delete)
            await session.commit()
            return order_to_delete
        return None