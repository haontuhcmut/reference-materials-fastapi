from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.item_type.service import ItemTypeService
from app.item_type.schema import CreateItemTypeModel, ItemTypeModel
from app.error import ItemTypeNotFound
from app.db.dependency import SessionDep

item_type_service = ItemTypeService()
item_type_route = APIRouter()


@item_type_route.get("/", response_model=list[ItemTypeModel])
async def get_all_type(session: SessionDep):
    item_type = await item_type_service.get_all_type(session)
    return item_type

@item_type_route.get("/{type_id}", response_model=ItemTypeModel)
async def get_type(type_id: str, session: SessionDep):
    item_type = await item_type_service.get_type(type_id, session)
    if item_type is None:
        raise ItemTypeNotFound()
    return item_type

@item_type_route.post("/", response_model=ItemTypeModel)
async def create_type(data_type: CreateItemTypeModel, session: SessionDep):
    new_type = await item_type_service.create_type(data_type, session)
    return new_type

@item_type_route.put("/{type_id}", response_model=ItemTypeModel)
async def update_type(type_id: str, data_update: CreateItemTypeModel, session: SessionDep):
    updated_type = await item_type_service.update_type(type_id, data_update, session)
    if updated_type is None:
        raise ItemTypeNotFound()
    return updated_type

@item_type_route.delete("/{type_id}")
async def delete_type(type_id: str, session: SessionDep):
    deleted_type = await item_type_service.delete_type(type_id, session)
    if deleted_type is None:
        raise ItemTypeNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The item type is deleted successfully"},
    )
