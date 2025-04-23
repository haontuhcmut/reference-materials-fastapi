from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CreateMaterialModel(BaseModel):
    material_code: str = Field(default=None, max_length=32)
    name: str = Field(default="Oatmeal/Strain", max_length=128)
    detailed_info: str | None = Field(default="lyophilized", max_length=1028)

class MaterialModel(CreateMaterialModel):
    id: UUID
    created_at: datetime