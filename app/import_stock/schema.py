from pydantic import BaseModel, Field
from uuid import UUID



class CreateImportStock(BaseModel):
    warehouse_id: UUID
    item_type_id: UUID

class ImportStockModel(CreateImportStock):
    id: UUID

