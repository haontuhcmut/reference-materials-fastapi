from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.order_item.service import OrderItemService
from app.order_item.schema import OrderItemModel, CreateOrderItemModel
from app.db.dependency import SessionDep
from app.error import OrderItemNotFound


order_item_service = OrderItemService()
order_item_route = APIRouter()

@order_item_route.get("/", response_model=list[OrderItemModel])
async def get_all_order_item(session: SessionDep):
    order_item = await order_item_service.get_all_order_item(session)
    return order_item

@order_item_route.get("/{order_item_id}", response_model=OrderItemModel)
async def get_order_item(order_item_id, session: SessionDep):
    order_item = await order_item_service.get_order_item(order_item_id, session)
    if order_item is None:
        raise OrderItemNotFound()
    return order_item

@order_item_route.post("/", response_model=OrderItemModel)
async def create_order_item(order_item_data: CreateOrderItemModel, session: SessionDep):
    new_order_item = await order_item_service.create_order_item(order_item_data, session)
    return new_order_item

@order_item_route.put("/{order_item_id}", response_model=OrderItemModel)
async def udpate_order_item(order_item_id: str, update_data: CreateOrderItemModel, session: SessionDep):
    updated_order_item = await order_item_service.update_order_item(order_item_id, update_data, session)
    if updated_order_item is None:
        raise OrderItemNotFound()
    return updated_order_item

@order_item_route.delete("/{order_item_id}")
async def delete_order_item(order_item_id: str, session: SessionDep):
    deleted_order_item = await order_item_service.delete_order_item(order_item_id, session)
    if deleted_order_item is None:
        raise OrderItemNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The order item deleted successfully"},
    )

