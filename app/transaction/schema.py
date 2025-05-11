from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    IMPORT = "import"
    EXPORT = "export"


class TransactionDetailBase(BaseModel):
    warehouse_id: UUID
    product_id: UUID | None = Field(default=None)
    material_id: UUID | None = Field(default=None)
    quantity: float = Field(default=0, ge=0, le=99999)


class CreateTransactionDetail(BaseModel):
    transaction_type: TransactionType
    note: str | None = Field(default=None, max_length=1024)
    details: list[TransactionDetailBase]


class TransactionModel(BaseModel):
    id: UUID
    transaction_type: TransactionType
    note: str | None
    created_at: datetime

class TransactionDetailModel(TransactionDetailBase):
    id: UUID

class TransactionDetailRespond(BaseModel):
    transaction: TransactionModel
    detail: list[TransactionDetailModel]