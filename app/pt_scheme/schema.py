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

