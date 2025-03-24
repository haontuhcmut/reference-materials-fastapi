from pydantic import BaseModel, Field
from datetime import date
from app.sample.schemas import CreateSampleSchema
import uuid


class CreateDeliveryPlanSchema(BaseModel):
    sample_id: uuid.UUID | None = Field(default=None)
    created_at: date
    delivery_date: date
    condition: str | None = Field(default=None, max_length=1024)


class DeliveryPlanResponseSchema(CreateDeliveryPlanSchema):
    delivery_id: uuid.UUID


class DeliveryPlanSampleSchema(DeliveryPlanResponseSchema, CreateSampleSchema):
    method: str | None = Field(default=None)
    pass
