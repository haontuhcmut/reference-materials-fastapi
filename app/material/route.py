from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.material.service import MaterialService
from app.error import MaterialNotFound
from app.material.schema import CreateMaterialModel, MaterialModel
from app.db.dependency import SessionDep

material_service = MaterialService()
material_route = APIRouter()


@material_route.get("/", response_model=list[MaterialModel])
async def get_all_material(session: SessionDep):
    material = await material_service.get_all_material(session)
    return material

@material_route.get("/{material_id}", response_model=MaterialModel)
async def get_material_item(material_id: str, session: SessionDep):
    material = await material_service.get_material_item(material_id, session)
    if material is None:
        raise MaterialNotFound()
    return material

@material_route.post("/", response_model=MaterialModel)
async def create_material(material_data: CreateMaterialModel, session:SessionDep):
    new_material = await material_service.create_material(material_data, session)
    return new_material

@material_route.put("/{material_id}", response_model=MaterialModel)
async def update_material(material_id: str, data_update: CreateMaterialModel, session: SessionDep):
    updated_material = await material_service.update_material(material_id, data_update, session)
    if updated_material is None:
        raise MaterialNotFound()
    return updated_material

@material_route.delete("/{material_id}", response_model=MaterialModel)
async def delete_material(material_id: str, session: SessionDep):
    deleted_material = await material_service.delte_material(material_id, session)
    if deleted_material is None:
        raise MaterialNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The material is deleted successfully"},
    )
