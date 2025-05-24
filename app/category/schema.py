from uuid import UUID
from pydantic import BaseModel, Field


class CreateCategoryModel(BaseModel):
    name: str = Field(max_length=128)

class CategoryModel(CreateCategoryModel):
    id: UUID

