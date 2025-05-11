from fastapi import APIRouter
from typing import Any

from app.db.dependency import SessionDep
from app.transaction.service import TransactionService
from app.transaction.schema import TransactionDetailRespond, CreateTransactionDetail, TransactionModel


transaction_service = TransactionService()
transaction_route = APIRouter()


@transaction_route.get("/", response_model=list[TransactionModel])
async def get_all_transaction(session: SessionDep):
    transactions = await transaction_service.get_all_transactions(session)
    return transactions

@transaction_route.get("/{transaction_id}", response_model=TransactionModel)
async def get_transaction_item(transaction_id: str, session: SessionDep):
    transaction = await transaction_service.get_transaction_item(transaction_id, session)
    return transaction

@transaction_route.post("/", response_model=TransactionDetailRespond)
async def create_transaction_detail(transaction_data: CreateTransactionDetail, session:SessionDep) -> Any:
    new_transaction = await transaction_service.create_transaction_detail(transaction_data, session)
    return new_transaction

