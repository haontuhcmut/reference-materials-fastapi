from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime

class StatusReportRead(BaseModel):
    id: UUID
    status: str
    description: Optional[str]


class SampleDeliveryRead(BaseModel):
    id: UUID
    created_at: datetime
    delivery_date: date
    description: Optional[str]
    status_reports: List[StatusReportRead] = []


class DHRead(BaseModel):
    id: UUID
    code: str
    status_reports: List[StatusReportRead] = []


class SampleRead(BaseModel):
    id: UUID
    sku: str
    name: str
    description: Optional[str]
    created_at: datetime
    deliveries: List[SampleDeliveryRead] = []
    dhs: List[DHRead] = []
    status_reports: List[StatusReportRead] = []
