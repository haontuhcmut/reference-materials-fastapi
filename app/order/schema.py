from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CreateOrderModel(BaseModel):
    customer_name: str = Field(default=None, max_length=64)

class OrderModel(CreateOrderModel):
    id: UUID
    order_time: datetime
