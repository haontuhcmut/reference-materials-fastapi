from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID
from fastapi import HTTPException, status

from app.db.model import Transaction, TransactionDetail, Inventory
from app.transaction.schema import CreateTransactionDetail, TransactionType
from app.product.route import product_service
from app.material.route import material_service
from app.warehouse.route import warehouse_service
from app.error import ProductNotFound, MaterialNotFound, WarehouseNotFound


class TransactionService:
    async def get_all_transactions(self, session:AsyncSession):
        statement = select(Transaction).order_by(desc(Transaction.created_at))
        results = await session.exec(statement)
        transactions = results.all()
        return transactions

    async def get_transaction_item(self, transaction_id: str, session: AsyncSession):
        transaction_uuid = UUID(transaction_id)
        statement = select(Transaction).where(Transaction.id == transaction_uuid)
        result = await session.exec(statement)
        transaction = result.first()
        return transaction

    async def create_transaction(self, transaction_data: CreateTransactionDetail, session: AsyncSession):
        product_id = transaction_data.product_id
        material_id = transaction_data.material_id
        warehouse_id = transaction_data.warehouse_id

        if not product_id and not material_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either product_id or material_id must be provided."
            )

        if product_id:
            product = await product_service.get_product_item(product_id)
            if product is None:
                raise ProductNotFound()

        if material_id:
            material = await material_service.get_material_item(material_id)
            if material is None:
                raise MaterialNotFound()

        if warehouse_id:
            warehouse = await warehouse_service.get_warehouse_item(warehouse_id)
            if warehouse is None:
                raise WarehouseNotFound()

        new_transaction = Transaction(
            transaction_type=transaction_data.transaction_type,
            note=transaction_data.note
        )
        session.add(new_transaction)
        await session.flush()

        data_dict = transaction_data.model_dump(exclude={'transaction_type', 'note'})
        new_transaction_detail = TransactionDetail(**data_dict, transaction_id=new_transaction.id)
        session.add(new_transaction_detail)

        # Refactored inventory update logic
        async def update_inventory(item_field: str, is_import: bool):
            item_id = getattr(transaction_data, item_field)
            if not item_id:
                return

            stmt = select(Inventory).where(getattr(Inventory, item_field) == item_id)
            result = await session.exec(stmt)
            inventory = result.first()

            if is_import:
                if inventory:
                    inventory.quantity += new_transaction_detail.quantity
                else:
                    session.add(Inventory(**data_dict))
            else:
                if not inventory:
                    raise HTTPException(
                        status_code=404,
                        detail=f"{item_field} not found in stock"
                    )
                if inventory.quantity < new_transaction_detail.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Insufficient {item_field} quantity in stock"
                    )
                inventory.quantity -= new_transaction_detail.quantity

        is_import = new_transaction.transaction_type == TransactionType.IMPORT
        is_export = new_transaction.transaction_type == TransactionType.EXPORT

        if is_import or is_export:
            await update_inventory('product_id', is_import)
            await update_inventory('material_id', is_import)

        await session.commit()
        return new_transaction










