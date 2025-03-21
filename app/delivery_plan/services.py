import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import DeliveryPlan
from sqlmodel import desc, select
from app.delivery_plan.schemas import CreateDeliveryPlan

class DeliveryPlanServices:
    async def get_delivery_plan(self, session: AsyncSession):
        statement = select(DeliveryPlan).order_by(desc(DeliveryPlan.created_at))
        results = await session.exec(statement)
        delivery_plan = results.all()
        return delivery_plan

    async def get_delivery_plan_item(self, delivery_id: str, session: AsyncSession):
        delivery_uuid = uuid.UUID(delivery_id)
        statement = select(DeliveryPlan).where(DeliveryPlan.id == delivery_uuid)
        result = await session.exec(statement)
        delivery_plan = result.first()
        return delivery_plan

    async def create_delivery_plan(self, delivery_data: CreateDeliveryPlan, session: AsyncSession):
        delivery_data_dict = delivery_data.model_dump()
        new_delivery = DeliveryPlan(**delivery_data_dict)
        session.add(new_delivery)
        await session.commit()
        return new_delivery

    async def update_delivery_plan(self, delivery_id: str, data_update: CreateDeliveryPlan, session: AsyncSession):
        delivery_to_update = await self.get_delivery_item(delivery_id, session)
        if delivery_to_update is not None:
            update_data_dict = data_update.model_dump()
            for key, value in update_data_dict.items():
                setattr(delivery_to_update, key, value)
            await session.commit()
            return delivery_to_update
        else:
            return None

    async def delete_delivery_plan(self, delivery_id: str, session: AsyncSession):
        delivery_to_delete = await self.get_delivery_plan_item(delivery_id, session)
        if delivery_to_delete is not None:
            await session.delete(delivery_to_delete)
            await session.commit()
            return delivery_to_delete
        else:
            return None
