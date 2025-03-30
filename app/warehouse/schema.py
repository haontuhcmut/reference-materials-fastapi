from uuid import UUID
from pydantic import BaseModel, Field


class CreateWarehouseModel(BaseModel):
    name: str = Field(default="Freezer warehouse", max_length=128)
    location: str = Field(default="ABC Floor, XYZ Street, Vietnam", max_length=128)
    type: str = Field(default="Freezer", max_length=32)


class WarehouseModel(CreateWarehouseModel):
    id: UUID
