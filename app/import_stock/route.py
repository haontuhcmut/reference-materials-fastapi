from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.import_stock.schema import CreateImportStock, ImportStockModel
from app.error import ImportStockNotFound
from app.import_stock.service import ImportStockService
from app.db.dependency import SessionDep

import_stock_service = ImportStockService()
import_stock_route = APIRouter()


@import_stock_route.get("/", response_model=list[ImportStockModel])
async def get_all_import_stock(session: SessionDep):
    import_stock = await import_stock_service.get_all_import_stock(session)
    return import_stock

@import_stock_route.get("/{import_id}", response_model=ImportStockModel)
async def get_import_stock_item(import_id: str, session: SessionDep):
    import_stock = await import_stock_service.get_import_stock_item(import_id, session)
    if import_stock is None:
        raise ImportStockNotFound()
    return import_stock

@import_stock_route.post("/", response_model=ImportStockModel)
async def create_import_stock(import_data: CreateImportStock, session: SessionDep):
    new_import_stock = await import_stock_service.create_import_stock(import_data, session)
    return new_import_stock

@import_stock_route.put("/{import_id}", response_model=ImportStockModel)
async def update_import_stock(import_id: str, data_update: CreateImportStock, session: SessionDep):
    updated_import_stock = await import_stock_service.update_import_stock(import_id, data_update, session)
    if updated_import_stock is None:
        raise ImportStockNotFound()
    return updated_import_stock

@import_stock_route.delete("/{import_id}")
async def delete_import_stock(import_id: str, session: SessionDep):
    deleted_import_stock = await import_stock_service.delete_import_stock(import_id, session)
    if deleted_import_stock is None:
        raise ImportStockNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "The import stock is deleted successfully"
        }
    )

