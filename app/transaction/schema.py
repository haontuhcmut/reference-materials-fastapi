from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    IMPORT = "import"
    EXPORT = "export"

class CreateTransaction(BaseModel):
    transaction_type: TransactionType
    note: str | None = Field(default=None, max_length=1024)

class TransactionModel(CreateTransaction):
    id: UUID
    created_at: datetime


