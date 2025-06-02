from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID
from fastapi import HTTPException, status

from app.db.model import (
    Transaction,
    TransactionDetail,
    Inventory,
    Product,
    Material,
    Warehouse,
)
from app.error import InvalidIDFormat

from app.transaction.schema import (
    TransactionType,
    CreateTransactionDetail,
    TransactionDetailModel,
    TransactionDetailRespond,
)


class TransactionService:
    async def get_all_transactions(self, session: AsyncSession):
        statement = select(Transaction).order_by(desc(Transaction.created_at))
        results = await session.exec(statement)
        transactions = results.all()
        return transactions

    async def get_transaction_item(self, transaction_id: str, session: AsyncSession):
        try:
            transaction_uuid = UUID(transaction_id)
        except ValueError:
            raise InvalidIDFormat()

        transaction = await session.get(Transaction, transaction_uuid)
        return transaction

    async def create_transaction_detail(
        self, transaction_data: CreateTransactionDetail, session: AsyncSession
    ):
        async with session.begin():
            new_transaction_dict = transaction_data.model_dump(exclude={"details"})
            new_transaction = Transaction(**new_transaction_dict)
            session.add(new_transaction)
            await session.flush()  # Needed to get transaction_id

            detail_result = []

            # Details looping
            for index, detail in enumerate(transaction_data.details, start=1):
                if not detail.product_id and not detail.material_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Item {index}: Either product_id or material_id is required.",
                    )

                if detail.product_id and detail.material_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Item {index}: Provide only one of product_id or material_id, not both.",
                    )

                if detail.warehouse_id:
                    warehouse = await session.get(Warehouse, detail.warehouse_id)
                    if warehouse is None:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item {index}: Warehouse {detail.warehouse_id} not found",
                        )

                if detail.product_id:
                    product = await session.get(Product, detail.product_id)
                    if product is None:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item {index}: Product {detail.product_id} not found",
                        )

                if detail.material_id:
                    material = await session.get(Material, detail.material_id)
                    if material is None:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Line {index}: Material {detail.material_id} not found",
                        )
                # Create transaction details
                detail_dict = detail.model_dump(exclude={"transaction_type", "note"})
                new_detail = TransactionDetail(
                    **detail_dict, transaction_id=new_transaction.id
                )
                session.add(new_detail)
                detail_result.append(new_detail)

                # Inventory available checking
                statement = select(Inventory).where(
                    Inventory.warehouse_id == detail.warehouse_id,
                    (
                        Inventory.product_id == detail.product_id
                        if detail.product_id
                        else Inventory.material_id == detail.material_id
                    ),
                )
                result = await session.exec(statement)
                inventory = result.first()

                # Import handling
                if transaction_data.transaction_type == TransactionType.IMPORT:
                    if inventory:
                        inventory.quantity += detail.quantity
                    else:
                        new_inventory = Inventory(**detail_dict)
                        session.add(new_inventory)

                # Export handling
                elif transaction_data.transaction_type == TransactionType.EXPORT:
                    if not inventory:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Item {index}: Item not found in inventory.",
                        )
                    if inventory.quantity < detail.quantity:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Item {index}: Not enough stock.",
                        )
                    inventory.quantity -= detail.quantity

        return TransactionDetailRespond(
            id=new_transaction.id,
            transaction_type=new_transaction.transaction_type,
            note=new_transaction.note,
            created_at=new_transaction.created_at,
            details=[
                TransactionDetailModel(
                    id=d.id,
                    warehouse_id=d.warehouse_id,
                    product_id=d.product_id,
                    material_id=d.material_id,
                    quantity=d.quantity,
                )
                for d in detail_result
            ],
        )

    async def get_all_transaction_details(self, session: AsyncSession):
        statement = (
            select(Transaction, TransactionDetail)
            .join(Transaction, Transaction.id == TransactionDetail.transaction_id)
            .order_by(desc(Transaction.created_at))
        )
        result = await session.exec(statement)
        rows = result.all()

        grouped = {}
        for trans, detail in rows:
            if trans.id not in grouped:
                grouped[trans.id] = {
                    "id": trans.id,
                    "transaction_type": trans.transaction_type,
                    "note": trans.note,
                    "created_at": trans.created_at,
                    "details": [],
                }
            grouped[trans.id]["details"].append(
                {
                    "id": detail.id,
                    "warehouse_id": detail.warehouse_id,
                    "quantity": detail.quantity,
                    "product_id": detail.product_id,
                    "material_id": detail.material_id,
                }
            )
        return list(grouped.values())
