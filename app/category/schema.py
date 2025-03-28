from uuid import UUID

from pydantic import BaseModel, Field


class CreateCategoryModel(BaseModel):
    name: str | None = Field(default=None, max_length=128)

class CategoryModel(CreateCategoryModel):
    id: UUID
