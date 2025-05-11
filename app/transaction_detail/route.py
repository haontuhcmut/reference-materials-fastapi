from fastapi import APIRouter

from app.transaction_detail.service import TransactionDetailService
from app.db.dependency import SessionDep

transaction_detail_service = TransactionDetailService()

transaction_detail_route = APIRouter()

@transaction_detail_route.get("/")
async def get_all_transaction_detail(session: SessionDep):
    transaction_detail = await transaction_detail_service.get_all_transaction_detail(session)
    return transaction_detail