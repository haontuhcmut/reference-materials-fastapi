from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.db.models import Sample, SampleDelivery, Dh, StatusReport

class InfoSampleServices:
    async def get_info_samples(self, session: AsyncSession):
        statement = (
            select(Sample)
            .options(
                selectinload(Sample.sample_deliveries).selectinload(SampleDelivery.status_reports),
                selectinload(Sample.dhs).selectinload(Dh.status_report),
                selectinload(Sample.status_reports)
            )
        )
        results = await session.exec(statement)
        samples = results.all()
        return samples
