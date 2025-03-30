from pydantic import BaseModel, Field
from uuid import UUID


class CreateMaterialModel(BaseModel):
    item_id: UUID
    internal_code: str = Field(default="MT-MC-01F/ST-MC-01F")
    name: str = Field(default="Oatmeal/Strain", max_length=128)
    quantity: float = Field(default=0, ge=0, le=99999)
    unit: str | None = Field(default="vial/tube/kg/g", max_length=16)
    detailed_info: str | None = Field(default="lyophilized", max_length=1028)

class MaterialModel(CreateMaterialModel):
    id: UUID