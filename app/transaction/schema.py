from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum


class TransactionType(str, Enum):
    IMPORT = "import"
    EXPORT = "export"


class ItemTransaction(BaseModel):
    item_type_id: UUID
    quantity: float = Field(default=0, ge=0, le=99999)

class CreateTransactionsModel(BaseModel):
    warehouse_id: UUID
    item_type_id: list[ItemTransaction]
    transaction_type: TransactionType
    description: str = Field(default=None, max_length=1024)