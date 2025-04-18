from pydantic import BaseModel, Field
from uuid import UUID


class StockInModel(BaseModel):
    item_type_id: UUID
    warehouse_id: UUID
