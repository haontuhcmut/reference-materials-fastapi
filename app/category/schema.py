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

    sort: list[str] | None = None

    class Constants(Filter.Constants):
        model = Category
        # The name of the query parameter used for sorting in the API.
        # Change this value to customize the sort parameter in your endpoints.
        ordering_field_name = "sort"
