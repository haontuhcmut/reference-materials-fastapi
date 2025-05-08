from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    IMPORT = "import"
    EXPORT = "export"

class Transaction(BaseModel):
    transaction_type: TransactionType
    note: str | None = Field(default=None, max_length=1024)

class CreateTransactionDetail(Transaction):
    transaction_id: UUID
    warehouse_id: UUID
    product_id: UUID | None = Field(default=None)
    material_id: UUID | None = Field(default=None)
    quantity: float = Field(default=0, ge=0, le=99999)

class TransactionDetailModel(CreateTransactionDetail):
    id: UUID
    created_at: datetime


