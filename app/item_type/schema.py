from uuid import UUID

from pydantic import BaseModel, Field


class CreateItemTypeModel(BaseModel):
    type_name: str | None = Field(default="Matrix/Strain", max_length=128)

class ItemTypeModel(CreateItemTypeModel):
    id: UUID
