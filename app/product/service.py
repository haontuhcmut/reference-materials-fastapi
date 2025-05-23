from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from uuid import UUID

from app.db.model import Product, Category, PTScheme, BillOfMaterial
from app.product.schema import CreateProductModel, ProductModelResponse, ProductItemDetailResponse, MaterialNameBase
from app.error import InvalidIDFormat, ProductNotFound, ProductAlreadyExist


class ProductService:
    async def get_all_product(self, session: AsyncSession):
        statement = (select(Product)
                     .options(selectinload(Product.pt_scheme))
                     .order_by(desc(Product.created_at))
                     )
        results = await session.exec(statement)
        products = results.all()
        product_response = [
            ProductModelResponse(
                **product.model_dump(),
                pt_scheme_code=product.pt_scheme.pt_scheme_code,
                analytes=product.pt_scheme.analytes,
                pt_name=product.pt_scheme.name,
            )
            for product in products
        ]
        return product_response

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
                selectinload(Product.bill_of_materials).selectinload(BillOfMaterial.material),
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
            "pt_scheme_code": product.pt_scheme.pt_scheme_code if product.pt_scheme else None,
            "pt_name": product.pt_scheme.name if product.pt_scheme else None,
            "analytes": product.pt_scheme.analytes if product.pt_scheme else None,
            "product_code": product.product_code,
            "sample_name": product.name,  # Using alias
            "created_at": product.created_at,
            "category_name": product.pt_scheme.category.name if product.pt_scheme and product.pt_scheme.category else None,
            "bill_of_materials": [
                {
                    "material_code": bom.material.material_code,
                    "material_name": bom.material.name
                }
                for bom in product.bill_of_materials
                if bom.material
            ],
            "quantity": product.inventory.quantity if product.inventory else 0.0,
            "unit": product.unit
        }

        return ProductItemDetailResponse.model_validate(response_data)

    async def get_from_product_code(self, product_code: str, session:AsyncSession):
        statement = select(Product).where(Product.product_code == product_code)
        result = await session.exec(statement)
        product = result.first()
        return product

    async def create_product(self, product_data: CreateProductModel, session: AsyncSession):
        product_code_exist = await self.get_from_product_code(product_data.product_code, session)
        if product_code_exist is not None:
            raise ProductAlreadyExist()
        data_dict = product_data.model_dump()
        new_product = Product(**data_dict)
        session.add(new_product)
        await session.commit()
        return new_product

    async def update_product(self, product_id: str, data_update: CreateProductModel, session: AsyncSession):
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise InvalidIDFormat()

        product_code_exist = await self.get_from_product_code(data_update.product_code, session)

        if product_code_exist:
            raise ProductAlreadyExist()
        statement = select(Product).where(Product.id == product_uuid)
        result = await session.exec(statement)
        product_to_update = result.first()

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










