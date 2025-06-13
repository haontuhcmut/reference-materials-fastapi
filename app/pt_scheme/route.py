from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params
from typing import Annotated

from app.pt_scheme.service import PTSchemeService
from app.error import PTSChemeNotFound
from app.db.dependency import SessionDep
from app.pt_scheme.schema import CreatePTSchemeModel, PTSchemeWithCategoryModel
from app.db.model import PTScheme

pt_scheme_service = PTSchemeService()
pt_scheme_route = APIRouter()


@pt_scheme_route.get("/", response_model=Page[PTScheme])
async def get_all_scheme(_params: Annotated[Params, Depends()], session: SessionDep):
    results = await pt_scheme_service.get_all_pt_scheme(session)
    return results

@pt_scheme_route.get("/{scheme_id}", response_model=PTSchemeWithCategoryModel)
async def get_scheme_item(scheme_id: str, session: SessionDep):
    result = await pt_scheme_service.get_scheme_item(scheme_id, session)
    if result is None:
        raise PTSChemeNotFound()
    scheme_id, category_name = result
    response_data = scheme_id.model_dump()
    response_data["category_name"] = category_name
    return PTSchemeWithCategoryModel.model_validate(response_data)

@pt_scheme_route.post("/", response_model=PTSchemeWithCategoryModel)
async def create_scheme(scheme_data: CreatePTSchemeModel, session: SessionDep):
    new_scheme, category_name = await pt_scheme_service.create_scheme(scheme_data, session)
    return PTSchemeWithCategoryModel(**new_scheme.model_dump(), category_name=category_name)

@pt_scheme_route.put("/{scheme_id}", response_model=PTSchemeWithCategoryModel)
async def update_scheme(scheme_id: str, data_update: CreatePTSchemeModel, session: SessionDep):
    update_result = await pt_scheme_service.update_scheme(scheme_id, data_update, session)
    if update_result is None:
        raise PTSChemeNotFound()
    updated_scheme, category_name = update_result
    return PTSchemeWithCategoryModel(**updated_scheme.model_dump(), category_name=category_name)

@pt_scheme_route.delete("/{scheme_id}")
async def delete_scheme(scheme_id: str, session: SessionDep):
    deleted_scheme = await pt_scheme_service.delete_scheme(scheme_id, session)
    if deleted_scheme is None:
        raise PTSChemeNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The PT Scheme deleted successfully"}
    )
