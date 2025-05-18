from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, timezone

class CreatePTSchemeModel(BaseModel):
    category_id: UUID
    pt_scheme_code: str = Field(default=None, max_length=32)
    name: str = Field(default=" Food Microbiology (QMS)", max_length=128)
    year: int | None = Field(default=None, ge=1900, le=2100)
    analytes: str | None = Field(default="Detection of Salmonella species", max_length=128)

class PTSchemeModel(CreatePTSchemeModel):
    id: UUID

class PTSchemeWithCategoryModel(BaseModel):
    id: UUID
    pt_scheme_code: str
    name: str = Field(alias="pt_name")
    category_name: str
    year: int
    analytes: str

    class Config:
        populate_by_name = True #relate alias




