from pydantic import BaseModel, Field
from enum import Enum
import uuid


class StatusEnum(str, Enum):
    pending = "pending"
    waiting = "waiting"
    finished = "finished"

class CreateStatusReportScheme(BaseModel):
    delivery_id: uuid.UUID | None = Field(default=None)
    status: StatusEnum = Field(default="pending")
    description: str | None = Field(default=None, min_length=1, max_length=1024)
