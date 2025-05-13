from uuid import UUID
from pydantic import BaseModel, Field


class CreateCategoryModel(BaseModel):
    name: str | None = Field(default="Microbiology", max_length=128)

class CategoryModel(CreateCategoryModel):
    id: UUID

class PaginatedCategory(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: list[CategoryModel]