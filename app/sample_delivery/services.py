import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import SampleDelivery
from sqlmodel import desc, select
from app.sample_delivery.schemas import CreateSampleDelivery

class SampleDeliveryServices:
    async def get_deliveries(self, session: AsyncSession):
        statement = select(SampleDelivery).order_by(desc(SampleDelivery.created_at))
        results = await session.exec(statement)
        sample_deliveries = results.all()
        return sample_deliveries

    async def get_delivery_item(self, delivery_id: str, session: AsyncSession):
        delivery_uuid = uuid.UUID(delivery_id)
        statement = select(SampleDelivery).where(SampleDelivery.id == delivery_uuid)
        result = await session.exec(statement)
        sample_delivery = result.first()
        return sample_delivery

    async def create_delivery(self, delivery_data: CreateSampleDelivery, session: AsyncSession):
        delivery_data_dict = delivery_data.model_dump()
        new_delivery = SampleDelivery(**delivery_data_dict)
        session.add(new_delivery)
        await session.commit()
        return new_delivery

    async def update_delivery(self, delivery_id: str, data_update: CreateSampleDelivery, session: AsyncSession):
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
