from uuid import UUID
from pydantic import BaseModel, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from app.db.model import Category
from pydantic import field_validator


class CreateCategoryModel(BaseModel):
    name: str = Field(max_length=128)


class CategoryModel(CreateCategoryModel):
    id: UUID


class CategoryFilter(Filter):

    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Category
        
        ordering_field_name = "order_by"
