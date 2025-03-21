import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import StatusReport
from sqlmodel import desc, select
from app.status_report.schemas import CreateStatusReportScheme

class StatusReportServices:
    async def get_status_reports(self, session: AsyncSession):
        statement = select(StatusReport).order_by(desc(StatusReport.status))
        results = await session.exec(statement)
        status_reports = results.all()
        return status_reports

    async def get_status_report_item(self, status_reports_id: str, session: AsyncSession):
        status_report_uuid = uuid.UUID(status_reports_id)
        statement = select(StatusReport).where(StatusReport.id == status_report_uuid)
        result = await session.exec(statement)
        status_report = result.first()
        return status_report

    async def create_status_report(self, status_report_data: CreateStatusReportScheme, session: AsyncSession):
        status_report_data_dict = status_report_data.model_dump()
        new_status_report = StatusReport(**status_report_data_dict)
        session.add(new_status_report)
        await session.commit()
        return new_status_report

    async def update_status_report(self, status_report_id: str, data_update: CreateStatusReportScheme, session: AsyncSession):
        status_report_to_update = await self.get_status_report_item(status_report_id, session)
        if status_report_to_update is not None:
            update_data_dict = data_update.model_dump()
            for key, value in update_data_dict.items():
                setattr(status_report_to_update, key, value)
            await session.commit()
            return status_report_to_update
        else:
            return None

    async def delete_status_report(self, status_report_id: str, session: AsyncSession):
        status_report_to_delete = await self.get_status_report_item(status_report_id, session)
        if status_report_to_delete is not None:
            await session.delete(status_report_to_delete)
            await session.commit()
            return status_report_to_delete
        else:
            return None