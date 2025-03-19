from fastapi import APIRouter, HTTPException, status
from app.db.models import StatusReport
from app.db.dependencies import SessionDep
from app.status_report.services import StatusReportServices
from app.status_report.schemas import CreateStatusReportScheme


status_report_services = StatusReportServices()
status_report_route = APIRouter()


@status_report_route.get("/", response_model=list[StatusReport])
async def get_status_report(session: SessionDep):
    status_reports = await status_report_services.get_status_reports(session)
    return status_reports


@status_report_route.get("/{status_report_item}", response_model=StatusReport)
async def get_status_report_item(status_report_item: str, session: SessionDep):
    status_report = await status_report_services.get_status_report_item(
        status_report_item, session
    )
    if status_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Status report not found"
        )
    return status_report


@status_report_route.post("/", response_model=StatusReport)
async def create_status_report(
    status_report_data: CreateStatusReportScheme, session: SessionDep
) -> dict:
    new_status_report = await status_report_services.create_status_report(
        status_report_data, session
    )
    return new_status_report


@status_report_route.put("/{status_report_item}", response_model=StatusReport)
async def update_status_report(
    status_report_item: str, data_update: CreateStatusReportScheme, session: SessionDep
):
    updated_status_report = await status_report_services.update_status_report(
        status_report_item, data_update, session
    )
    if updated_status_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Status report not found"
        )
    else:
        return updated_status_report


@status_report_route.delete("/{status_report_item}", response_model=StatusReport)
async def delete_status_report(status_report_item: str, session: SessionDep):
    status_report_to_deleted = await status_report_services.delete_status_report(
        status_report_item, session
    )
    if status_report_to_deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Status report not found"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="Status report is deleted"
        )
