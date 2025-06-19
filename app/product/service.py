from unicodedata import category
from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from fastapi_pagination.ext.sqlmodel import apaginate
from fastapi_pagination import Page
from uuid import UUID

from app.db.model import Product, PTScheme, BillOfMaterial
from app.product.schema import (
    CreateProductModel,
    ProductItemDetailResponse,
)
from app.error import (
    InvalidIDFormat,
    ProductNotFound,
    ProductAlreadyExist,
    PTSChemeNotFound,
)


class ProductService:
    async def get_all_product(self, session: AsyncSession) -> Page[Product]:
        statement = select(Product).order_by(desc(Product.created_at))
        return await apaginate(session, statement)

    async def get_product_item(self, product_id: str, session: AsyncSession):
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise InvalidIDFormat()

        statement = (
            select(Product)
            .where(Product.id == product_uuid)
            .options(
                selectinload(Product.pt_scheme).selectinload(PTScheme.category),
                selectinload(Product.bill_of_materials).selectinload(
                    BillOfMaterial.material
                ),
                selectinload(Product.inventory),
            )
        )
        result = await session.exec(statement)
        product = result.first()

        if not product:
            raise ProductNotFound()

        # Build the response data explicitly
        response_data = {
            "id": product.id,
            "pt_scheme_code": (
                product.pt_scheme.pt_scheme_code if product.pt_scheme else None
            ),
            "pt_name": product.pt_scheme.name if product.pt_scheme else None,
            "analytes": product.pt_scheme.analytes if product.pt_scheme else None,
            "product_code": product.product_code,
            "sample_name": product.name,  # Using alias
            "created_at": product.created_at,
            "category_name": (
                product.pt_scheme.category.name
                if product.pt_scheme and product.pt_scheme.category
                else None
            ),
            "bill_of_materials": [
                {
                    "material_code": bom.material.material_code,
                    "material_name": bom.material.name,
                }
                for bom in product.bill_of_materials
                if bom.material
            ],
            "quantity": product.inventory.quantity if product.inventory else 0.0,
            "unit": product.unit,
        }

        return ProductItemDetailResponse.model_validate(response_data)

    async def get_from_product_code(self, product_code: str, session: AsyncSession):
        statement = select(Product).where(Product.product_code == product_code)
        result = await session.exec(statement)
        product = result.first()
        return product

    async def create_product(
        self, product_data: CreateProductModel, session: AsyncSession
    ):
        scheme = await session.get(PTScheme, product_data.pt_scheme_id)
        if scheme is None:
            raise PTSChemeNotFound()

        product_code_exist = await self.get_from_product_code(
            product_data.product_code, session
        )
        if product_code_exist:
            raise ProductAlreadyExist()

        data_dict = product_data.model_dump()
        new_product = Product(**data_dict)
        session.add(new_product)
        await session.commit()
        return new_product

    async def update_product(
        self, product_id: str, data_update: CreateProductModel, session: AsyncSession
    ):
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise InvalidIDFormat()

        product = await session.get(Product, product_uuid)
        if product is None:
            raise ProductNotFound()

        scheme = await session.get(PTScheme, data_update.pt_scheme_id)
        if scheme is None:
            raise PTSChemeNotFound()

        if product.product_code != data_update.product_code:
            statement = select(Product).where(
                Product.product_code == data_update.product_code,
                product.id != product_uuid,
            )
            result = await session.exec(statement)
            existing_product = result.first()
            if existing_product:
                raise ProductAlreadyExist()

        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        await session.commit()
        return product

    async def delete_product(self, product_id: str, session: AsyncSession):
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise InvalidIDFormat()

        product_to_delete = await session.get(Product, product_uuid)
        if product_to_delete is not None:
            await session.delete(product_to_delete)
            await session.commit()
            return product_to_delete
        return None
