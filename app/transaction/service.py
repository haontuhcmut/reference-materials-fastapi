from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID


from app.db.model import Transaction
from app.transaction.schema import CreateTransaction, TransactionModel


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

    async def create_transaction(self, transaction_data: CreateTransaction, session: AsyncSession):
        data_dict = transaction_data.model_dump()
        new_transaction = Transaction(**data_dict)
        session.add(new_transaction)
        await session.commit()
        return new_transaction



