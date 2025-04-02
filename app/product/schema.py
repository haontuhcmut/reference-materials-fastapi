from pydantic import BaseModel, Field
from datetime import datetime

from uuid import UUID

class CreateProductModel(BaseModel):
    item_type_id: UUID
    pt_scheme_id: UUID
    product_code: str = Field(default=None, max_length=32)
    name: str = Field(default="Salmonella sp. in food (Detection)", max_length=128)
    sku: str = Field(default="PT-MC-06F", max_length=128)
    status: str | None = Field(default=None, max_length=16)

class ProductModel(CreateProductModel):
    id: UUID
