from pydantic import BaseModel, Field
from uuid import UUID


class CreateBomModel(BaseModel):
    product_id: UUID
    material_id: UUID
    quantity_required: int = Field(default=0, ge=0, le=999)


class BomModel(CreateBomModel):
    id: UUID