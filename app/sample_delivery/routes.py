from fastapi import APIRouter, HTTPException, status
from app.db.models import SampleDelivery
from app.db.dependencies import SessionDep
from app.sample_delivery.services import SampleDeliveryServices
from app.sample_delivery.schemas import CreateSampleDelivery


delivery_services = SampleDeliveryServices()
sample_delivery_route = APIRouter()

@sample_delivery_route.get("/", response_model=list[SampleDelivery])
async def get_delivery(session: SessionDep):
    deliveries = await delivery_services.get_deliveries(session)
    return deliveries

@sample_delivery_route.get("/{delivery_item}", response_model=SampleDelivery)
async def get_delivery_item(delivery_item: str, session:SessionDep):
    delivery = await delivery_services.get_delivery_item(delivery_item, session)
    if delivery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample delivery not found")
    return delivery

@sample_delivery_route.post("/", response_model=SampleDelivery)
async def create_delivery(delivery_data: CreateSampleDelivery, session: SessionDep) -> dict:
    new_delivery = await delivery_services.create_delivery(delivery_data, session)
    return new_delivery

@sample_delivery_route.put("/{delivery_item}", response_model=SampleDelivery)
async def update_delivery(delivery_item: str, data_update: CreateSampleDelivery, session: SessionDep):
    updated_delivery = await delivery_services.update_delivery(delivery_item, data_update, session)
    if updated_delivery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample delivery not found")
    else:
        return updated_delivery

@sample_delivery_route.delete("/{delivery_item}", response_model=SampleDelivery)
async def delete_delivery(delivery_item: str, session: SessionDep):
    delivery_to_deleted = await delivery_services.delete_delivery(delivery_item, session)
    if delivery_to_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample delivery not found")
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Sample delivery is deleted")
