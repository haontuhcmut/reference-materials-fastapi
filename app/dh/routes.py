from fastapi import APIRouter, HTTPException, status
from app.db.models import Dh
from app.db.dependencies import SessionDep
from app.dh.services import DhServices
from app.dh.schemas import CreateDhScheme


dh_services = DhServices()
dh_route = APIRouter()

@dh_route.get("/", response_model=list[Dh])
async def get_dh(session: SessionDep):
    dh = await dh_services.get_dh(session)
    return dh

@dh_route.get("/{dh_item}", response_model=Dh)
async def get_dh_item(dh_item: str, session: SessionDep):
    dh = await dh_services.get_dh_item(dh_item, session)
    if dh is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dh not found")
    return dh

@dh_route.post("/", response_model=Dh)
async def create_dh(dh_data: CreateDhScheme, session: SessionDep) -> dict:
    new_dh = await dh_services.create_dh(dh_data, session)
    return new_dh

@dh_route.put("/{dh_item}", response_model=Dh)
async def update_dh(dh_item: str, data_update: CreateDhScheme, session: SessionDep):
    updated_dh = await dh_services.update_dh(dh_item, data_update, session)
    if updated_dh is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dh not found")
    else:
        return updated_dh

@dh_route.delete("/{dh_item}", response_model=Dh)
async def delete_dh(dh_item: str, session: SessionDep):
    dh_to_deleted = await dh_services.delete_dh(dh_item, session)
    if dh_to_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dh not found")
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Dh is deleted")
