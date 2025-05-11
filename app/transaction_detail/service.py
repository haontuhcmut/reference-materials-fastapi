from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.model import TransactionDetail, Transaction


class TransactionDetailService:
    async def get_all_transaction_detail(self, session: AsyncSession):
        statement = (
            select(TransactionDetail, Transaction)
            .join(Transaction, Transaction.id == TransactionDetail.transaction_id)
        )
        result = await session.exec(statement)
        rows = result.all()

        response = [
            {
                "transaction_id": trans.id,
                "transaction_type": trans.transaction_type,
                "note": trans.note,
                "created_at": trans.created_at,
                "warehouse_id": detail.warehouse_id,
                "quantity": detail.quantity,
                "product_id": detail.product_id,
                "material_id": detail.material_id
            }
            for detail, trans in rows
        ]
        return response
