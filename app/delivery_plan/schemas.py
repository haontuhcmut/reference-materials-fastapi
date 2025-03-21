from pydantic import BaseModel, Field
from datetime import date
import uuid

class CreateDeliveryPlan(BaseModel):
    sample_id: uuid.UUID | None = Field(default=None)
    created_at: date
    delivery_date: date
    description: str | None = Field(default=None, max_length=1024)

