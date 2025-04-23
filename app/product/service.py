from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.db.model import Product
from app.product.schema import CreateProductModel

class ProductService:
    async def get_all_product(self, session: AsyncSession):
        statement = select(Product).order_by(Product.name)
        results = await session.exec(statement)
        products = results.all()
        return products

    async def get_product_item(self, product_id: str, session: AsyncSession):
        product_uuid = UUID(product_id)
        statement = select(Product).where(Product.id == product_uuid)
        result = await session.exec(statement)
        product = result.first()
        return product

    async def create_product(self, product_data: CreateProductModel, session: AsyncSession):
        data_dict = product_data.model_dump()
        new_product = Product(**data_dict)
        session.add(new_product)
        await session.commit()
        return new_product

    async def update_product(self, product_id: str, data_update: CreateProductModel, session: AsyncSession):
        product_to_update = await self.get_product_item(product_id, session)
        if product_to_update is not None:
            data_dict = data_update.model_dump()
            for key, value in data_dict.items():
                setattr(product_to_update, key, value)
            await session.commit()
            return product_to_update
        return None

    async def delete_product(self, product_id: str, session: AsyncSession):
        product_to_delete = await self.get_product_item(product_id, session)
        if product_to_delete is not None:
            await session.delete(product_to_delete)
            await session.commit()
            return product_to_delete
        return None










