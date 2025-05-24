from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CreateMaterialModel(BaseModel):
    material_code: str = Field(max_length=32)
    name: str = Field(max_length=128)
    unit: str = Field(max_length=16)
    detailed_info: str | None = Field(default=None, max_length=1028)

class MaterialModel(CreateMaterialModel):
    id: UUID
    created_at: datetime

class BillOfMaterialBase(BaseModel):
    product_name: str
    product_code: str

class MaterialDetailResponse(MaterialModel):
    quantity_in_stock: float = Field(ge=0, le=99999)
    bill_of_materials: list[BillOfMaterialBase] | None

