from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params, paginate
from typing import Annotated

from app.warehouse.schema import CreateWarehouseModel, WarehouseModel, WarehouseDetailModel
from app.warehouse.service import WarehouseService
from app.error import WarehouseNotFound
from app.db.dependency import SessionDep

warehouse_service = WarehouseService()
warehouse_route = APIRouter()

@warehouse_route.get("/", response_model=Page[WarehouseModel])
async def get_all_warehouse(_params: Annotated[Params, Depends()], session: SessionDep):
    warehouse = await warehouse_service.get_all_warehouse(session)
    return paginate(warehouse)

@warehouse_route.get("/{warehouse_id}", response_model=WarehouseModel)
async def get_warehouse_detail(warehouse_id: str, session: SessionDep):
    warehouse = await warehouse_service.get_warehouse_item(warehouse_id, session)
    if warehouse is None:
        raise WarehouseNotFound()
    return warehouse

@warehouse_route.post("/", response_model=WarehouseModel)
async def create_warehouse(warehouse_data: CreateWarehouseModel, session: SessionDep):
    new_warehouse = await warehouse_service.create_warehouse(warehouse_data, session)
    return new_warehouse

@warehouse_route.put("/{warehouse_id}", response_model=WarehouseModel)
async def update_warehouse(warehouse_id: str, warehouse_data: CreateWarehouseModel, session: SessionDep):
    updated_warehouse = await warehouse_service.update_warehouse(warehouse_id, warehouse_data, session)
    if updated_warehouse is None:
        raise WarehouseNotFound()
    return updated_warehouse

@warehouse_route.delete("/{warehouse_id}", response_model=WarehouseModel)
async def delete_warehouse(warehouse_id: str, session: SessionDep):
    deleted_warehouse = await warehouse_service.delete_warehouse(warehouse_id, session)
    if deleted_warehouse is None:
        raise WarehouseNotFound()
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "The warehouse is deleted successfully"}
    )

