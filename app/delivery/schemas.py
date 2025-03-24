from pydantic import BaseModel, Field
import uuid
from datetime import date

class CreateDeliveryScheme(BaseModel):
    delivery_plan_id: uuid.UUID | None = Field(default=None)
    delivery_code: str = Field(default="KT3-00000BVS5", max_length=15)
    due_date: date | None = Field(default=None)
    created_at: date | None = Field(default=None)
