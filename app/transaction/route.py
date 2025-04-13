from fastapi import APIRouter

from app.transaction.service import TransactionService
from app.transaction.schema import TransactionModel, CreateTransactionsModel
from app.db.dependency import SessionDep
from app.error import TransactionNotFound

transaction_service = TransactionService()
transaction_route = APIRouter()


@transaction_route.get("/", response_model= list[TransactionModel])
async def get_transaction(session: SessionDep):
    transaction = await transaction_service.get_all_transaction(session)
    return transaction

@transaction_route.get("/{transaction_id}", response_model=TransactionModel)
async def get_transaction_item(transaction_id: str, session: SessionDep):
    transaction_item = await transaction_service.get_transaction_item(transaction_id, session)
    if transaction_item is None:
        raise TransactionNotFound()
    return transaction_item

@transaction_route.post("/", response_model=TransactionModel)
async def create_transaction(transaction_data: CreateTransactionsModel, session: SessionDep):
    new_transaction = await transaction_service.create_transaction_data(transaction_data, session)
    return new_transaction

@transaction_route.put("/{transaction_id}", response_model=TransactionModel)
async def update_transaction(transaction_id: str, data_update: CreateTransactionsModel, session: SessionDep):
    updated_transaction = await transaction_service.update_transaction_data(transaction_id, data_update, session)
    if updated_transaction is None:
        raise TransactionNotFound()
    return updated_transaction

@transaction_route.delete("/{transaction_id}", response_model=TransactionModel)
async def delete_transaction(transaction_id: str, session: SessionDep):
    deleted_transaction = await transaction_service.delete_transaction(transaction_id, session)
    if deleted_transaction is None:
        raise TransactionNotFound()
    return deleted_transaction





























