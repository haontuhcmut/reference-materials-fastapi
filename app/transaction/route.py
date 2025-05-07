from fastapi import APIRouter


from app.db.dependency import SessionDep
from app.transaction.service import TransactionService
from app.transaction.schema import TransactionModel, CreateTransaction


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

@transaction_route.post("/", response_model=TransactionModel)
async def create_tranasaction(transaction_data: CreateTransaction, session:SessionDep):
    new_transaction = await transaction_service.create_transaction(transaction_data, session)
    return new_transaction

