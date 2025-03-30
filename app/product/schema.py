from pydantic import BaseModel, Field
from datetime import datetime

from uuid import UUID

class CreateProductModel(BaseModel):
    item_type_id: UUID
    pt_scheme_id: UUID
    name: str = Field(default="Salmonella sp. in food (Detection)", max_length=128)
    sku: str = Field(default="PT-MC-06F", max_length=128)
    quantity: int = Field(default=0, ge=0, le=999)
    unit: str | None = Field(default=None, max_length=16)
    status: str | None = Field(default=None, max_length=16)

class ProductModel(CreateProductModel):
    id: UUID
