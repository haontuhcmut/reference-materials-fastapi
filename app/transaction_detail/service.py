from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.db.model import TransactionDetail



class TransactionDetailService:
    async def get_all_transaction_detail(self, session: AsyncSession):
        statement = select(TransactionDetail)
        results = await session.exec(statement)
        transaction_details = results.all()
        return transaction_details

    async def get_transaction_detail(self, transaction_detail_id: str, session: AsyncSession):
        transaction_detail_uuid = UUID(transaction_detail_id)
        statement = select(TransactionDetail).where(TransactionDetail.id == transaction_detail_uuid)
        results = await session.exec(statement)
        transaction_detail = results.frist()
        return transaction_detail

    async def create_transaction_detail(self, ):