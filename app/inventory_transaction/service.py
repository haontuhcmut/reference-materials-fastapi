from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc, and_
from uuid import UUID
from fastapi import HTTPException, status

from app.db.model import InventoryTransaction, Warehouse
from app.inventory_transaction.schema import (
    CreateExportImportStockModel,
    TransactionsType,
)
from app.error import WarehouseNotFound


class InventoryTransactionService:
    async def get_all_inventory_transactions(self, session: AsyncSession):
        statement = select(InventoryTransaction).order_by(
            desc(InventoryTransaction.created_at)
        )
        results = await session.exec(statement)
        inventories = results.all()
        return inventories

    async def get_inventory_transaction_item(
        self, inventory_transaction_id: str, session: AsyncSession
    ):
        inventory_transaction_uuid = UUID(inventory_transaction_id)
        statement = select(InventoryTransaction).where(
            InventoryTransaction == inventory_transaction_uuid
        )
        result = await session.exec(statement)
        inventory = result.first()
        return inventory

    async def export_import_stock(
            self, create_inventory: CreateExportImportStockModel, session: AsyncSession
    ):
        data_dict = create_inventory.model_dump()
        warehouse_id = data_dict["warehouse_id"]
        product_id = data_dict["product_id"]
        material_id = data_dict["material_id"]
        quantity = data_dict["quantity"]
        transaction_type = data_dict["transaction_type"]

        warehouse_result = await session.exec(
            select(Warehouse).where(Warehouse.id == warehouse_id)
        )
        warehouse = warehouse_result.first()
        if warehouse is None:
            raise WarehouseNotFound()

        if not material_id and not product_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Either material_id or product_id must be provided",
                    "error_code": "material_or_product_not_none",
                },
            )

        conditions = [InventoryTransaction.warehouse_id == warehouse_id]
        if material_id:
            conditions.append(InventoryTransaction.material_id == material_id)
        if product_id:
            conditions.append(InventoryTransaction.product_id == product_id)

        existing_stmt = select(InventoryTransaction).where(and_(*conditions))
        existing_result = await session.exec(existing_stmt)
        existing_transaction = existing_result.first()

        if transaction_type == TransactionsType.import_stock:
            if existing_transaction:
                existing_transaction.quantity += quantity
                transaction = existing_transaction
            else:
                transaction = InventoryTransaction(**data_dict)
                session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return transaction

        if transaction_type == TransactionsType.export_stock:
            if not existing_transaction:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No inventory transaction found for this export",
                )
            if quantity > existing_transaction.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The request must be less than the inventory",
                )
            existing_transaction.quantity -= quantity
            transaction = existing_transaction
            await session.commit()
            await session.refresh(transaction)
            return transaction

    async def delete_inventory_transaction(self, inventory_transaction_id: str, session: AsyncSession):
        inventory_to_delete = await self.get_inventory_transaction_item(inventory_transaction_id, session)
        if inventory_to_delete is not None:
            await session.delete(inventory_to_delete)
            await session.commit()
            return inventory_to_delete
        return None

