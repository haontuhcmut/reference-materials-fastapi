from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from uuid import UUID

class CreateProductModel(BaseModel):
    pt_scheme_id: UUID
    product_code: str = Field(default=None, max_length=32)
    name: str = Field(default="PT sample", max_length=128)

class ProductModel(CreateProductModel):
    id: UUID
    created_at: datetime

class ProductModelResponse(BaseModel):
    id: UUID
    pt_scheme_code: str
    pt_name: str
    analytes: str
    product_code: str
    name: str = Field(alias="sample_name")
    created_at: datetime

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True) #Fill origin name, but output alias name


class MaterialNameBase(BaseModel):
    material_code: str
    name: str = Field(alias="material_name")

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)


class ProductItemDetailResponse(ProductModelResponse):
    category_name: str
    bill_of_materials: list[MaterialNameBase]
    quantity: float




    



