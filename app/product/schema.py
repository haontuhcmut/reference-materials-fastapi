from pydantic import BaseModel, Field
from datetime import datetime

from uuid import UUID

class CreateProductModel(BaseModel):
    pt_scheme_id: UUID
    product_code: str = Field(default=None, max_length=32)
    name: str = Field(default="Salmonella sp. in food (Detection)", max_length=128)

class ProductModel(CreateProductModel):
    id: UUID
    created_at: datetime

class ProductModelResponse(BaseModel):
    id: UUID
    pt_scheme_code: str
    pt_name: str
    product_code: str
    name: str
    created_at: datetime

class ProductItemDetailResponse(ProductModelResponse):
    category_name: str



