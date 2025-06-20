from uuid import UUID
from pydantic import BaseModel, Field
from fastapi_filter.contrib.sqlalchemy import Filter
from app.db.model import Category


class CreateCategoryModel(BaseModel):
    name: str = Field(max_length=128)


class CategoryModel(CreateCategoryModel):
    id: UUID


class CategoryFilter(Filter):
    name: str | None = None
    name__ilike: str | None = None
    name_like: str | None = None
    name__neq: str | None = None

    search: str | None = None

    class Constants(Filter.Constants):
        model = Category
        search_model_fields = ["name"]
