from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params, paginate
from typing import Annotated

from app.bom.service import BomService
from app.db.dependency import SessionDep
from app.bom.schema import BomModel, CreateBomModel, BomModelResponse, BomDetailModelResponse
from app.error import BomNotFound


bom_service = BomService()
bom_route = APIRouter()

@bom_route.get("/", response_model=Page[BomModelResponse])
async def get_all_bom(params: Annotated[Params, Depends()], session: SessionDep):
    bom = await bom_service.get_all_bom(session=session, params=params)
    return bom

@bom_route.get("/{bom_id}", response_model=BomModelResponse)
async def get_bom_item(bom_id: str, session: SessionDep):
    bom_item = await bom_service.get_bom_item(bom_id, session)
    if bom_item is None:
        raise BomNotFound()
    return bom_item

@bom_route.get("/get_from_product/{product_id}", response_model=list[BomDetailModelResponse])
async def get_bom_detail_by_product_id(product_id: str, session: SessionDep):
    bom_detail = await bom_service.get_bom_from_product_id(product_id, session)
    if bom_detail is None:
        raise BomNotFound()
    return bom_detail


@bom_route.post("/", response_model=BomModel)
async def create_bom(bom_data: CreateBomModel, session: SessionDep):
    new_bom = await bom_service.create_bom_item(bom_data, session)
    return new_bom

@bom_route.put("/{bom_id}", response_model=BomModel)
async def update_bom(bom_id: str, data_update: CreateBomModel, session: SessionDep):
    updated_bom = await bom_service.update_bom(bom_id, data_update, session)
    if updated_bom is None:
        raise BomNotFound()
    return updated_bom

@bom_route.delete("/{bom_id}", response_model=BomModel)
async def delete_bom(bom_id: str, session: SessionDep):
    deleted_bom = await bom_service.delete_bom(bom_id, session)
    if deleted_bom is None:
        raise BomNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The bill of material is deleted successfully"},
    )
