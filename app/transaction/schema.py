from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum


class TransactionType(Enum):
    IMPORT = "import"
    EXPORT = "export"


class ItemList(BaseModel):
    item_type_id: UUID
    quantity: float = Field(default=0, ge=0, le=99999)

class CreateTransactionsModel(BaseModel):
    warehouse_id: UUID
    item_type_id: list[ItemList]
    transaction_type: TransactionType
    description: str = Field(default=None, max_length=1024)

# class CreateTransactionModel(BaseModel):
#     warehouse_id: UUID
#     item_type_id: UUID
#     transaction_type: str = Field(default=None, max_length=64)
#     quantity: float = Field(default=0, ge=0, le=99999)
#     description: str = Field(default=None, max_length=1024)
#
#
# class TransactionModel(CreateTransactionModel):
#     id: UUID
