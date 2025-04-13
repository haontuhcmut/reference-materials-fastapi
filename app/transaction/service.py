from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Field, select
from uuid import UUID

from app.db.model import Transaction, Inventory, ItemType, Warehouse
from app.transaction.schema import CreateTransactionsModel, TransactionType
from app.item_type.service import ItemTypeService
from app.warehouse.service import WarehouseService
from app.error import WarehouseNotFound, ItemTypeNotFound

item_type_service = ItemTypeService()
warehouse_service = WarehouseService()


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

    async def create_transaction(
        self, transaction_data: CreateTransactionsModel, session: AsyncSession
    ):
        







