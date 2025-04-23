from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.order.service import OrderService
from app.order.schema import OrderModel, CreateOrderModel
from app.db.dependency import SessionDep
from app.error import OrderNotFound


order_service = OrderService()
order_route = APIRouter()


@order_route.get("/", response_model=list[OrderModel])
async def get_all_order(session: SessionDep):
    order = await order_service.get_all_order(session)
    return order


@order_route.get("/{order_id}", response_model=OrderModel)
async def get_order_item(order_id: str, session: SessionDep):
    order = await order_service.get_order_item(order_id, session)
    if order is None:
        raise OrderNotFound()
    return order


@order_route.post("/", response_model=OrderModel)
async def create_order(order_data: CreateOrderModel, session: SessionDep):
    new_order = await order_service.create_order(order_data, session)
    return new_order


@order_route.put("/{order_id}", response_model=OrderModel)
async def update_order(
    order_id: str, update_data: CreateOrderModel, session: SessionDep
):
    updated_order = await order_service.update_order(order_id, update_data, session)
    if updated_order is None:
        raise OrderNotFound()
    return updated_order


@order_route.delete("/{order_id}")
async def delete_order(order_id: str, session: SessionDep):
    deleted_order = await order_service.delete_order(order_id, session)
    if deleted_order is None:
        raise OrderNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The order deleted successfully"},
    )
