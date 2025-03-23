from pydantic import BaseModel, Field
import uuid
from datetime import date

class CreateDeliveryScheme(BaseModel):
    delivery_code: str = Field(default=None, max_length=15)
    due_date: date | None = Field(default=None)
    created_at: date | None = Field(default=None)
