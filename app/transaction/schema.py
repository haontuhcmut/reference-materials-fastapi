from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum


class TransactionType(Enum):
    IMPORT = "import"
    EXPORT = "export"


class CreateTransactionsModel(BaseModel):
    warehouse_id: UUID
    item_type_id: UUID
    transaction_type: TransactionType
    quantity: float = Field(default=0, ge=0, le=99999)
    description: str = Field(default=None, max_length=1024)

class TransactionModel(CreateTransactionsModel):
    id: UUID

class ImportStockModel(BaseModel):
    item_type_id: UUID
    warehouse_id: UUID
    transaction_type: TransactionType.IMPORT
    quantity: float = Field(default=0, ge=0, le=99999)
    description: str | None = Field(default=None, max_length=1024)

class ExportStockModel(BaseModel):
    item_type_id: UUID
    warehouse_id: UUID
    transaction_type: TransactionType.EXPORT
    quantity: float = Field(default=0, ge=0, le=99999)
    description: str | None = Field(default=None, max_length=1024)

