from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from uuid import UUID

from app.db.model import ImportStock
from app.import_stock.schema import CreateImportStock


class ImportStockService:
    async def get_all_import_stock(self, session: AsyncSession):
        statement = select(ImportStock).order_by(desc(ImportStock.created_at))
        results = await session.exec(statement)
        import_stock = results.all()
        return import_stock

    async def get_import_stock_item(self, import_id: str, session: AsyncSession):
        import_uuid = UUID(import_id)
        statement = select(ImportStock).where(ImportStock.id == import_id)
        result = await session.exec(statement)
        import_stock = result.first()
        return import_stock

    async def create_import_stock(self, import_data: CreateImportStock, session: AsyncSession):
        data_dict = import_data.model_dump()
        new_import = ImportStock(**data_dict)
        session.add(new_import)
        await session.commit()
        return new_import

    async def update_import_stock(self, import_id: str, data_update: CreateImportStock, session: AsyncSession):
        update_to_import_stock = await self.get_import_stock_item(import_id, session)
        if update_to_import_stock is not None:
            data_dict = data_update.model_dump()
            for key, value in data_dict.items():
                setattr(update_to_import_stock, key, value)
            await session.commit()
            return update_to_import_stock
        return None

    async def delete_import_stock(self, import_id: str, session: AsyncSession):
        delete_to_import_stock = await self.get_import_stock_item(import_id, session)
        if delete_to_import_stock is not None:
            await session.delete(delete_to_import_stock)
            await session.commit()
            return delete_to_import_stock
        return None