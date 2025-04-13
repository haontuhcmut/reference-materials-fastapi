from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID
from fastapi import HTTPException, status

from app.transaction.schema import (
    CreateTransactionsModel,
    ImportStockModel,
    ExportStockModel,
)
from app.db.model import Transaction, Inventory


class TransactionService:
    async def get_all_transaction(self, session: AsyncSession):
        statement = select(Transaction).order_by(Transaction.transaction_type)
        results = await session.exec(statement)
        transactions = results.all()
        return transactions

    async def get_transaction_item(self, transaction_id: str, session: AsyncSession):
        transaction_uuid = UUID(transaction_id)
        statement = select(Transaction).where(Transaction.id == transaction_uuid)
        result = await session.exec(statement)
        transaction = result.first()
        return transaction

    async def import_stock(
        self, import_stock_data: ImportStockModel, session: AsyncSession
    ):
        data_dict = import_stock_data.model_dump()
        item_type_uuid = UUID(data_dict["item_type_id"])
        warehouse_uuid = UUID(data_dict["warehouse_id"])
        statement = select(Inventory).where(
            Inventory.item_type_id == item_type_uuid,
            Inventory.warehouse_id == warehouse_uuid,
        )
        results = await session.exec(statement)
        inventory = results.first()
        if inventory is None:
            inventory = Inventory(
                item_type_id=item_type_uuid, warehouse_id=warehouse_uuid, quantity=0
            )
            session.add(inventory)
        inventory.quantity += data_dict["quantity"]
        transaction = Transaction(**data_dict)
        session.add(transaction)
        await session.commit()
        return transaction

    async def export_stock(
        self, export_stock_data: ExportStockModel, session: AsyncSession
    ):
        data_dict = export_stock_data.model_dump()
        item_type_uuid = UUID(data_dict["item_type_id"])
        warehouse_uuid = UUID(data_dict["warehouse_id"])
        quantity = data_dict["quantity"]
        statement = select(Inventory).where(
            Inventory.item_type_id == item_type_uuid,
            Inventory.warehouse_id == warehouse_uuid,
        )
        results = await session.exec(statement)
        inventory = results.first()
        if inventory is not None:
            if quantity > inventory.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough inventory. Available: {inventory.quantity}",
                )
            else:
                new_quantity = inventory.quantity - quantity
                inventory = Inventory(quantity=new_quantity)
                session.add(inventory)
                await session.commit()
                return inventory
        return None

    async def update_transaction_data(
        self,
        transaction_id: str,
        data_update: CreateTransactionsModel,
        session: AsyncSession,
    ):
        transaction_to_update = await self.get_transaction_item(transaction_id, session)
        if transaction_to_update is not None:
            data_dict = transaction_to_update.model_dump()
            for key, value in data_dict.items():
                setattr(transaction_to_update, key, value)
            await session.commit()
            return transaction_to_update
        return None

    async def delete_transaction(self, transaction_id: str, session: AsyncSession):
        transaction_to_delete = await self.get_transaction_item(transaction_id, session)
        if transaction_to_delete is not None:
            await session.delete(transaction_to_delete)
            await session.commit()
            return transaction_to_delete
        return None
