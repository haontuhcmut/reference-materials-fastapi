from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.inventory_transaction.service import InventoryTransactionService
from app.db.dependency import SessionDep
from app.inventory_transaction.schema import (
    ExportImportStockModel,
    CreateExportImportStockModel,
)
from app.error import InventoryTransactionNotFound


inventory_transaction_service = InventoryTransactionService()
inventory_transaction_route = APIRouter()


@inventory_transaction_route.get("/", response_model=list[ExportImportStockModel])
async def get_all_inventory(session: SessionDep):
    inventories = await inventory_transaction_service.get_all_inventory_transactions(
        session
    )
    return inventories


@inventory_transaction_route.get(
    "/{inventory_transaction_id}", response_model=ExportImportStockModel
)
async def get_inventory_transaction_item(
    inventory_transaction_id: str, session: SessionDep
):
    inventory = await inventory_transaction_service.get_inventory_transaction_item(
        inventory_transaction_id, session
    )
    if inventory is None:
        raise InventoryTransactionNotFound()
    return inventory


@inventory_transaction_route.post("/", response_model=ExportImportStockModel)
async def create_inventory_transaction(
    create_inventory: CreateExportImportStockModel, session: SessionDep
):
    new_inventory = await inventory_transaction_service.export_import_stock(
        create_inventory, session
    )
    return new_inventory


@inventory_transaction_route.delete("/{inventory_transaction_id}")
async def delete_inventory_transaction(
    inventory_transaction_id: str, session: SessionDep
):
    deleted_inventory = (
        await inventory_transaction_service.delete_inventory_transaction(
            inventory_transaction_id, session
        )
    )
    if deleted_inventory is None:
        raise InventoryTransactionNotFound()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "The inventory is deleted successfully"},
    )
