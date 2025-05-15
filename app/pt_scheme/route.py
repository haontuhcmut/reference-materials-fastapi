from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params
from typing import Annotated

from app.pt_scheme.service import PTSchemeService
from app.error import PTSChemeNotFound
from app.db.dependency import SessionDep
from app.pt_scheme.schema import PTSchemeModel, CreatePTSchemeModel, PTSchemeWithCategoryModel

pt_scheme_service = PTSchemeService()
pt_scheme_route = APIRouter()


@pt_scheme_route.get("/", response_model=Page[PTSchemeWithCategoryModel])
async def get_all_scheme(params: Annotated[Params, Depends()], session: SessionDep):
    pt_scheme = await pt_scheme_service.get_all_pt_scheme(session)
    return pt_scheme

@pt_scheme_route.get("/{scheme_id}", response_model=PTSchemeModel)
async def get_scheme_item(scheme_id: str, session: SessionDep):
    scheme_item = await pt_scheme_service.get_scheme_item(scheme_id, session)
    if scheme_item is None:
        raise PTSChemeNotFound()
    return scheme_item

@pt_scheme_route.post("/", response_model=PTSchemeModel)
async def create_scheme(scheme_data: CreatePTSchemeModel, session: SessionDep):
    new_scheme = await pt_scheme_service.create_scheme(scheme_data, session)
    return new_scheme

@pt_scheme_route.put("/{scheme_id}", response_model=PTSchemeModel)
async def update_scheme(scheme_id: str, data_update: CreatePTSchemeModel, session: SessionDep):
    updated_scheme = await pt_scheme_service.update_scheme(scheme_id, data_update, session)
    if updated_scheme is None:
        raise PTSChemeNotFound
    return updated_scheme

@pt_scheme_route.delete("/{scheme_id}")
async def delete_scheme(scheme_id: str, session: SessionDep):
    deleted_scheme = await pt_scheme_service.delete_scheme(scheme_id, session)
    if deleted_scheme is None:
        raise PTSChemeNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The PT Scheme deleted successfully"}
    )
