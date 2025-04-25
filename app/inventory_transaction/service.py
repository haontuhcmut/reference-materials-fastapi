from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc, and_
from uuid import UUID
from fastapi import HTTPException, status

from app.db.model import InventoryTransaction, Warehouse, Product, Material
from app.inventory_transaction.schema import (
    CreateExportImportStockModel,
    TransactionsType,
)
from app.error import WarehouseNotFound, ProductNotFound, MaterialNotFound


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

        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Quantity must be greater than zero",
                },
            )

        # Validate warehouse
        warehouse = await session.get(Warehouse, warehouse_id)
        if not warehouse:
            raise WarehouseNotFound()

        # Validate product
        product = await session.get(Product, product_id) if product_id else None
        if product_id and not product:
            raise ProductNotFound()

        # Validate material
        material = await session.get(Material, material_id) if material_id else None
        if material_id and not material:
            raise MaterialNotFound()

        # Material or product must be provided
        if not material and not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Either a valid material or product must be provided",
                },
            )

        # Material or product, not both
        if material is not None and product is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Only one of material or product should be provided.",
                },
            )

        # Build filter conditions
        conditions = [InventoryTransaction.warehouse_id == warehouse_id]
        if material:
            conditions.append(InventoryTransaction.material_id == material_id)
        if product:
            conditions.append(InventoryTransaction.product_id == product_id)

        # Query existing inventory transaction
        stmt = select(InventoryTransaction).where(and_(*conditions))
        result = await session.exec(stmt)
        existing_transaction = result.first()

        if transaction_type == TransactionsType.import_stock:
            if existing_transaction:
                existing_transaction.quantity += quantity
                transaction = existing_transaction
            else:
                transaction = InventoryTransaction(**data_dict)
                session.add(transaction)

        elif transaction_type == TransactionsType.export_stock:
            if not existing_transaction:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No inventory transaction found for this export",
                )
            if quantity > existing_transaction.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The request must be less than or equal to the inventory",
                )
            existing_transaction.quantity -= quantity
            transaction = InventoryTransaction(**data_dict)
            session.add(transaction)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Invalid transaction type"},
            )
        await session.commit()
        return transaction

    async def delete_inventory_transaction(
        self, inventory_transaction_id: str, session: AsyncSession
    ):
        inventory_to_delete = await self.get_inventory_transaction_item(
            inventory_transaction_id, session
        )
        if inventory_to_delete is not None:
            await session.delete(inventory_to_delete)
            await session.commit()
            return inventory_to_delete
        return None
