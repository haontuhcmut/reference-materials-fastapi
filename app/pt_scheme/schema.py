from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class CreatePTSchemeModel(BaseModel):
    category_id: UUID
    pt_scheme_code: str = Field(max_length=32)
    name: str = Field(max_length=128)
    year: int = Field(ge=1900, le=2100)
    analytes: str = Field(max_length=128)

class PTSchemeModel(CreatePTSchemeModel):
    id: UUID

class PTSchemeWithCategoryModel(BaseModel):
    id: UUID
    pt_scheme_code: str
    name: str = Field(alias="pt_name")
    category_name: str | None
    year: int
    analytes: str

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

