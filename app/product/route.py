from typing import Annotated, Any

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params, paginate

from app.product.schema import CreateProductModel, ProductModelResponse
from app.product.service import ProductService
from app.error import ProductNotFound
from app.db.dependency import SessionDep

product_service = ProductService()
product_route = APIRouter()


@product_route.get("/", response_model=Page[ProductModelResponse])
async def get_all_product(_params: Annotated[Params, Depends()], session: SessionDep):
    products = await product_service.get_all_product(session)
    return paginate(products)


@product_route.get("/{product_id}")
async def get_product_item(product_id: str, session: SessionDep):
    product = await product_service.get_product_item(product_id, session)
    if product is None:
        raise ProductNotFound()
    return product


@product_route.post("/")
async def create_product(product_data: CreateProductModel, session: SessionDep):
    new_product = await product_service.create_product(product_data, session)
    return new_product


@product_route.put("/{product_id}")
async def update_product(
    product_id: str, data_update: CreateProductModel, session: SessionDep
):
    updated_product = await product_service.update_product(
        product_id, data_update, session
    )
    if updated_product is None:
        raise ProductNotFound()
    return updated_product


@product_route.delete("/{product_id}")
async def delete_product(product_id: str, session: SessionDep):
    deleted_product = await product_service.delete_product(product_id, session)
    if deleted_product is None:
        raise ProductNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The product deleted successfully"},
    )
