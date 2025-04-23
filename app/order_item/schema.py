from pydantic import BaseModel, Field
from uuid import UUID

class CreateOrderItemModel(BaseModel):
    order_id: UUID | None = Field(default=None)
    product_id: UUID | None = Field(default=None)
    quantity: float = Field(default=0, ge=0, le=99999)

class OrderItemModel(CreateOrderItemModel):
    id: UUID
