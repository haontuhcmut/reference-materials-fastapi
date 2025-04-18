from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Field, select
from uuid import UUID
from fastapi import HTTPException, status

from app.db.model import Transaction, Inventory
from app.transaction.schema import CreateTransactionsModel, TransactionType
from app.item_type.service import ItemTypeService
from app.error import ItemTypeNotFound

item_type_service = ItemTypeService()


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

    async def create_import_request(
        self, transaction_data: CreateTransactionsModel, session: AsyncSession
    ):
        for item in transaction_data.items:
            item_type_id = item.item_type_id
            quantity = item.quantity

            if transaction_data.transaction_type.IMPORT:
                item_type = await item_type_service.get_type(item_type_id, session)
                if item_type is None:
                    raise ItemTypeNotFound()











