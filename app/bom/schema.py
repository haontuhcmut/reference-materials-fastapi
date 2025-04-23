from pydantic import BaseModel, Field
from uuid import UUID


class CreateBomModel(BaseModel):
    product_id: UUID
    material_id: UUID


class BomModel(CreateBomModel):
    id: UUID