from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from app.sample.schemas import CreateSampleScheme
from app.delivery_plan.schemas import CreateDeliveryPlanScheme
from app.delivery.schemas import CreateDeliveryScheme
from app.status_report.schemas import CreateStatusReportScheme


class ReadDelivery(CreateDeliveryPlanScheme):
    id: UUID

class ReadDh(CreateDeliveryScheme):
    id: UUID

class ReadStatus(CreateStatusReportScheme):
    id: UUID

class SampleRead(CreateSampleScheme):
    id: UUID
    deliveries: List[ReadDelivery] | None = None
    # dhs: List[ReadDh] | None = None
    # status_reports: List[ReadStatus] | None = None

