from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class TransactionsType(str, Enum):
    import_stock = "import_stock"
    export_stock = "export_stock"


class CreateExportImportStockModel(BaseModel):
    warehouse_id: UUID
    product_id: UUID | None = Field(default=None)
    material_id: UUID | None = Field(default=None)
    order_id: UUID | None = Field(default=None)
    quantity: float = Field(default=0, ge=0, le=99999)
    transaction_type: TransactionsType
    description: str | None = Field(default=None, max_length=1024)


class ExportImportStockModel(CreateExportImportStockModel):
    id: UUID
    created_at: datetime



