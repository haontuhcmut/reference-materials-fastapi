import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import Delivery
from sqlmodel import desc, select
from app.delivery.schemas import CreateDeliveryScheme

class DeliveryServices:
    async def get_delivery(self, session: AsyncSession):
        statement = select(Delivery).order_by(desc(Delivery.delivery_code))
        results = await session.exec(statement)
        delivery = results.all()
        return delivery

    async def get_delivery_item(self, delivery_id: str, session: AsyncSession):
        delivery_uuid = uuid.UUID(delivery_id)
        statement = select(Delivery).where(Delivery.id == delivery_uuid)
        result = await session.exec(statement)
        delivery = result.first()
        return delivery

    async def create_delivery(self, delivery_data: CreateDeliveryScheme, session: AsyncSession):
        delivery_data_dict = delivery_data.model_dump()
        new_delivery = Delivery(**delivery_data_dict)
        session.add(new_delivery)
        await session.commit()
        return new_delivery

    async def update_delivery(self, delivery_id: str, data_update: CreateDeliveryScheme, session: AsyncSession):
        delivery_to_update = await self.get_delivery_item(delivery_id, session)
        if delivery_to_update is not None:
            update_data_dict = data_update.model_dump()
            for key, value in update_data_dict.items():
                setattr(delivery_to_update, key, value)
            await session.commit()
            return delivery_to_update
        else:
            return None

    async def delete_delivery(self, delivery_id: str, session: AsyncSession):
        delivery_to_delete = await self.get_delivery_item(delivery_id, session)
        if delivery_to_delete is not None:
            await session.delete(delivery_to_delete)
            await session.commit()
            return delivery_to_delete
        else:
            return None
