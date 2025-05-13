from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    IMPORT = "import"
    EXPORT = "export"


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    note: str | None


class TransactionModel(TransactionBase):
    id: UUID
    created_at: datetime


class TransactionDetailBase(BaseModel):
    warehouse_id: UUID
    product_id: UUID | None = Field(default=None)
    material_id: UUID | None = Field(default=None)
    quantity: float = Field(default=0, ge=0, le=99999)


class TransactionDetailModel(TransactionDetailBase):
    id: UUID


class CreateTransactionDetail(TransactionBase):
    details: list[TransactionDetailBase]


class TransactionDetailRespond(TransactionModel):
    details: list[TransactionDetailModel]
