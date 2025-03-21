from fastapi import APIRouter, HTTPException, status
from app.db.models import Delivery
from app.db.dependencies import SessionDep
from app.delivery.services import DeliveryServices
from app.delivery.schemas import CreateDeliveryScheme


delivery_services = DeliveryServices()
delivery_route = APIRouter()

@delivery_route.get("/", response_model=list[Delivery])
async def get_delivery(session: SessionDep):
    dh = await delivery_services.get_delivery(session)
    return dh

@delivery_route.get("/{dh_item}", response_model=Delivery)
async def get_delivery_item(delivery_item: str, session: SessionDep):
    delivery = await delivery_services.get_delivery_item(delivery_item, session)
    if delivery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dh not found")
    return delivery

@delivery_route.post("/", response_model=Delivery)
async def create_delivery(delivery_data: CreateDeliveryScheme, session: SessionDep) -> dict:
    new_delivery = await delivery_services.create_delivery(delivery_data, session)
    return new_delivery

@delivery_route.put("/{delivery_item}", response_model=Dh)
async def update_delivery(delivery_item: str, data_update: CreateDeliveryScheme, session: SessionDep):
    updated_delivery = await delivery_services.update_delivery(dh_item, data_update, session)
    if updated_delivery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    else:
        return updated_delivery

@delivery_route.delete("/{delivery_item}", response_model=Dh)
async def delete_delivery(delivery_item: str, session: SessionDep):
    delivery_to_deleted = await delivery_services.delete_delivery(delivery_item, session)
    if delivery_to_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Delivery is deleted")
