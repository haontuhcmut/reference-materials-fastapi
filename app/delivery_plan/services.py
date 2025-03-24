import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import DeliveryPlan, Sample
from sqlmodel import desc, select, asc

from app.delivery_plan.schemas import CreateDeliveryPlanSchema, DeliveryPlanSampleSchema
from datetime import date


class DeliveryPlanServices:
    async def get_delivery_plan(self, session: AsyncSession):
        statement = (
            select(DeliveryPlan, Sample)
            .join(Sample)
            .where(Sample.id == DeliveryPlan.sample_id)
        )
        results = await session.exec(statement)
        rows = results.all()
        delivery_plans = [
            DeliveryPlanSampleSchema(
                delivery_id=delivery_plan.id,
                sample_id=delivery_plan.sample_id,
                created_at=delivery_plan.created_at,
                condition=delivery_plan.condition,
                delivery_date=delivery_plan.delivery_date,
                sku=sample.sku,
                name=sample.name,
                method=sample.method,
            )
            for delivery_plan, sample in rows
        ]
        return delivery_plans

    async def get_delivery_plan_today(self, session: AsyncSession):
        today = date.today()
        statement = (
            select(DeliveryPlan, Sample)
            .join(Sample)
            .where(DeliveryPlan.delivery_date == today)
        )
        results = await session.exec(statement)
        rows = results.all()
        delivery_plan_today = [
            DeliveryPlanSampleSchema(
                delivery_id=delivery_plan.id,
                sample_id=delivery_plan.sample_id,
                created_at=delivery_plan.created_at,
                condition=delivery_plan.condition,
                delivery_date=delivery_plan.delivery_date,
                sku=sample.sku,
                name=sample.name,
                method=sample.method,
            )
            for delivery_plan, sample in rows
        ]
        return delivery_plan_today

    async def get_delivery_plan_item(
        self, delivery_plan_id: str, session: AsyncSession
    ):
        delivery_plan_uuid = uuid.UUID(delivery_plan_id)
        statement = (
            select(DeliveryPlan, Sample)
            .join(Sample)
            .where(DeliveryPlan.id == delivery_plan_uuid)
        )
        result = await session.exec(statement)
        delivery_plans = (
            DeliveryPlanSampleSchema(
                delivery_id=delivery_plan.id,
                sample_id=delivery_plan.sample_id,
                created_at=delivery_plan.created_at,
                condition=delivery_plan.condition,
                delivery_date=delivery_plan.delivery_date,
                sku=sample.sku,
                name=sample.name,
                method=sample.method,
            )
            for delivery_plan, sample in result
        )
        return delivery_plans

    async def create_delivery_plan(
        self, delivery_plan_data: CreateDeliveryPlanSchema, session: AsyncSession
    ):
        delivery_plan_data_dict = delivery_plan_data.model_dump()
        new_delivery_plan = DeliveryPlan(**delivery_plan_data_dict)
        session.add(new_delivery_plan)
        await session.commit()
        return new_delivery_plan

    async def get_delivery_plan_base_on_id(
        self, delivery_plan_id: str, session: AsyncSession
    ):
        delivery_plan_uuid = uuid.UUID(delivery_plan_id)
        statement = select(DeliveryPlan).where(DeliveryPlan.id == delivery_plan_uuid)
        results = await session.exec(statement)
        delivery_plan = results.first()
        return delivery_plan

    async def update_delivery_plan(
        self,
        delivery_plan_id: str,
        data_update: CreateDeliveryPlanSchema,
        session: AsyncSession,
    ):
        delivery_to_update = await self.get_delivery_plan_item(
            delivery_plan_id, session
        )
        if delivery_to_update is not None:
            update_data_dict = data_update.model_dump()
            for key, value in update_data_dict.items():
                setattr(delivery_to_update, key, value)
            await session.commit()
            return delivery_to_update
        else:
            return None

    async def delete_delivery_plan(self, delivery_plan_id: str, session: AsyncSession):
        delivery_to_delete = await self.get_delivery_plan_base_on_id(
            delivery_plan_id, session
        )
        if delivery_to_delete is not None:
            await session.delete(delivery_to_delete)
            await session.commit()
            return delivery_to_delete
        else:
            return None
