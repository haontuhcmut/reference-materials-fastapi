from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_filter import FilterDepends, with_prefix
from fastapi import Query

from app.db.model import PTScheme, Category


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


class CategoryFilter(Filter):
    name__ilike: str | None = None

    class Constants(Filter.Constants):
        model: Category

class PTSchemesFilter(Filter):
    name__ilike: str | None = None
    pt_scheme_code__ilike: str | None = None
    year: int | None = None
    year__gte: int | None = None
    year__lte: int | None = None

    category: CategoryFilter | None = FilterDepends(
        with_prefix("category", CategoryFilter)
    )

    # search: str | None = Field(
    #     Query(description="Search by scheme code, name and analytic")
    # )

    class Constants(Filter.Constants):
        model = PTScheme
        # search_model_fields = ["name", "pt_scheme_code", "analytes"]
