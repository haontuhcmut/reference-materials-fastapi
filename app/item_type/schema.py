from uuid import UUID

from pydantic import BaseModel, Field


class CreateItemTypeModel(BaseModel):
    item_type_code: str = Field(default=None, max_length=32)
    name: str = Field(default=None, max_length=32)
    item_type: str = Field(default=None, max_length=128)
    unit: str = Field(default=None, max_length=16)

class ItemTypeModel(CreateItemTypeModel):
    id: UUID
