from fastapi import APIRouter, HTTPException, status
from app.db.models import DeliveryPlan
from app.db.dependencies import SessionDep
from app.delivery_plan.services import DeliveryPlanServices
from app.delivery_plan.schemas import CreateDeliveryPlan


delivery_services = DeliveryPlanServices()
delivery_plan_route = APIRouter()

@delivery_plan_route.get("/", response_model=list[DeliveryPlan])
async def get_delivery_plan(session: SessionDep):
    delivery_plan = await delivery_services.get_delivery_plan(session)
    return delivery_plan

@delivery_plan_route.get("/{delivery_plan_item}", response_model=DeliveryPlan)
async def get_delivery_plan_item(delivery_plan_item: str, session:SessionDep):
    delivery_plan = await delivery_services.get_delivery_plan_item(delivery_plan_item, session)
    if delivery_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery plan not found")
    return delivery_plan

@delivery_plan_route.post("/", response_model=DeliveryPlan)
async def create_delivery_plan(delivery_plan_data: CreateDeliveryPlan, session: SessionDep) -> dict:
    new_delivery_plan = await delivery_services.create_delivery_plan(delivery_plan_data, session)
    return new_delivery_plan

@delivery_plan_route.put("/{delivery_plan_item}", response_model=DeliveryPlan)
async def update_delivery_plan(delivery_plan_item: str, data_update: CreateDeliveryPlan, session: SessionDep):
    updated_delivery = await delivery_services.update_delivery_plan(delivery_plan_item, data_update, session)
    if updated_delivery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery plan not found")
    else:
        return updated_delivery

@delivery_plan_route.delete("/{delivery_plan_item}", response_model=DeliveryPlan)
async def delete_delivery_plan(delivery_plan_item: str, session: SessionDep):
    delivery_to_deleted = await delivery_services.delete_delivery_plan(delivery_plan_item, session)
    if delivery_to_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery plan not found")
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Delivery plan is deleted")
