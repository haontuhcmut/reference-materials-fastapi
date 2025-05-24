from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union

class CreateWarehouseModel(BaseModel):
    name: str = Field(max_length=128)
    location: str = Field(max_length=128)
    type: str = Field(max_length=32)


class WarehouseModel(CreateWarehouseModel):
    id: UUID


class MaterialBase(BaseModel):
    type: str = "material"
    material_code: str
    material_name: str

class ProductBase(BaseModel):
    type: str = "product"
    product_code: str
    product_name: str

class InventoryBase(BaseModel):
    id: UUID
    quantity: float
    last_update: datetime
    item_detail: list[Union[ProductBase, MaterialBase]] = None

class WarehouseDetailModel(WarehouseModel):
    inventories: list[InventoryBase]

