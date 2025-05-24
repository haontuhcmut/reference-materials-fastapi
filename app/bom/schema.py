from pydantic import BaseModel, Field
from uuid import UUID


class CreateBomModel(BaseModel):
    product_id: UUID
    material_id: UUID
    quantity_per_product: float = Field(ge=0.0, le=99999)
    unit_per_product: str = Field(max_length=32)


class BomModel(CreateBomModel):
    id: UUID


class BomModelResponse(BaseModel):
    id: UUID
    product_id: UUID
    product_code: str
    material_id: UUID
    material_code: str

class MaterialBase(BaseModel):
    material_id: UUID
    material_code: str
    material_name: str
    quantity_per_product: float = Field(ge=0.0, le=99999)
    unit_per_product: str = Field(max_length=32)

class BomDetailModelResponse(BomModel):
    product_code: str
    product_name: str
    material_code: str
    material_name: str


