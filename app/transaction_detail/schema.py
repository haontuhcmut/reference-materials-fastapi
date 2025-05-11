from pydantic import BaseModel, Field
from uuid import UUID


class CreateTransactionDetail(BaseModel):
    transaction_id: UUID
    warehouse_id: UUID
    product_id: UUID | None = Field(default=None)
    material_id: UUID | None = Field(default=None)
    quantity: float = Field(default=0, ge=0, le=99999)