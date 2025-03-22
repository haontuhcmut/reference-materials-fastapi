import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import Sample
from sqlmodel import desc, select
from app.sample.schemas import CreateSampleScheme

class SampleServices:
    async def get_samples(self, session: AsyncSession):
        statement = select(Sample).order_by(desc(Sample.created_at))
        results = await session.exec(statement)
        samples = results.all()
        return samples

    async def get_sample_item(self, sample_id: str, session: AsyncSession):
        sample_uuid = uuid.UUID(sample_id)
        statement = select(Sample).where(Sample.id == sample_uuid)
        result = await session.exec(statement)
        sample = result.first()
        return sample

    async def get_sample_sku(self, sample_sku: str, session: AsyncSession):
        statement = select(Sample).where(Sample.sku == sample_sku)
        result = await session.exec(statement)
        sample = result.all()
        return sample

    async def create_sample(self, sample_data: CreateSampleScheme, session: AsyncSession):
        sample_data_dict = sample_data.model_dump()
        new_sample = Sample(**sample_data_dict)
        session.add(new_sample)
        await session.commit()
        return new_sample

    async def update_sample(self, sample_id: str, data_update: CreateSampleScheme, session: AsyncSession):
        sample_to_update = await self.get_sample_item(sample_id, session)
        if sample_to_update is not None:
            update_data_dict = data_update.model_dump()
            for key, value in update_data_dict.items():
                setattr(sample_to_update, key, value)
            await session.commit()
            return sample_to_update
        else:
            return None

    async def delete_sample(self, sample_id: str, session: AsyncSession):
        sample_to_delete = await self.get_sample_item(sample_id, session)
        if sample_to_delete is not None:
            await session.delete(sample_to_delete)
            await session.commit()
            return sample_to_delete
        else:
            return None
