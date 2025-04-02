from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Field, select
from uuid import UUID

from app.db.model import Transaction, Inventory
from app.transaction.schema import CreateTransactionsModel, TransactionType


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
        self, import_request_data: CreateTransactionsModel, session: AsyncSession
    ):
        transactions = []

        for item in import_request_data.item_type_id:
            item_type_id, quantity = item["item_type_id"], item["quantity"]

            if import_request_data.transaction_type == TransactionType.IMPORT:
                statement = select(Inventory).where(
                    Inventory.warehouse_id == import_request_data.warehouse_id,
                    Inventory.item_type_id == item_type_id,
                )
                result = await session.exec(statement)
                inventory = result.first()
                if inventory:
                    inventory.quantity += quantity
                else:
                    inventory = Inventory(
                        warehouse_id=import_request_data.warehouse_id,
                        item_type_id=item_type_id,
                        quantity=quantity,
                    )
                    session.add(inventory)

            transaction = Transaction(
                warehouse_id=import_request_data.warehouse_id,
                item_type_id=item_type_id,
                quantity=quantity,
                transaction_type=import_request_data.transaction_type,
                description=import_request_data.description,
            )
            session.add(transaction)
            transactions.append(transaction)
        await session.commit()
        return transactions

    # async def create_export_request(
    #     self, export_request_data: CreateTransactionsModel, session: AsyncSession
    # ):
    #     for item in export_request_data.item_type_id:
    #         item_type_id, quantity = item["item_type_id"], item["quantity"]
    #
    #         statement = select(Inventory.quantity).where(
    #             Inventory.warehouse_id == export_request_data.warehouse_id,
    #             Inventory.item_type_id == item_type_id,
    #         )


