from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from app.db.dependency import SessionDep
from app.category.service import CategoryService
from app.category.schema import CategoryModel, CreateCategoryModel
from app.error import CategoryNotFound

category_service = CategoryService()
category_route = APIRouter()


@category_route.get("/", response_model=list[CategoryModel])
async def get_all_category(session: SessionDep):
    categories = await category_service.get_all_category(session)
    return categories


@category_route.get("/{category_id}", response_model=CategoryModel)
async def get_category_item(category_id: str, session: SessionDep):
    category = await category_service.get_category_item(category_id, session)
    if category is None:
        raise CategoryNotFound()
    return category


@category_route.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CategoryModel
)
async def create_category(category_data: CreateCategoryModel, session: SessionDep):
    new_category = await category_service.create_category(category_data, session)
    return new_category


@category_route.put("/{category_id}", response_model=CategoryModel)
async def update_category(category_id: str, data_update: CreateCategoryModel, session: SessionDep):
    updated_category = await category_service.update_category(category_id, data_update, session)
    if updated_category is None:
        raise CategoryNotFound()
    return updated_category


@category_route.delete("/{category_id}")
async def category_delete(category_id: str, session: SessionDep):
    deleted_category = await category_service.delete_category(category_id, session)
    if deleted_category is None:
        raise CategoryNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The category is deleted successfully"},
    )
