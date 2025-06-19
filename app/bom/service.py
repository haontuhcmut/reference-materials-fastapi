from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from sqlalchemy.orm import selectinload
from fastapi_pagination.ext.sqlmodel import apaginate
from fastapi_pagination import Page, Params
from typing import Annotated
from fastapi import Depends

from app.db.model import BillOfMaterial, Product, Material
from app.bom.schema import (
    CreateBomModel,
    BomModelResponse,
    BomDetailModelResponse,
)
from app.error import ProductNotFound, MaterialNotFound, InvalidIDFormat, BomNotFound


class BomService:
    async def get_all_bom(self, params: Params, session: AsyncSession):
        statement = (
            select(BillOfMaterial)
            .options(
                selectinload(BillOfMaterial.product),
                selectinload(BillOfMaterial.material),
            )
            .join(BillOfMaterial.product)
            .order_by(desc(Product.created_at))  # Order by Product's created_at
            .offset(params.to_raw_params().offset)
            .limit(params.to_raw_params().limit)
        )

        result = await session.exec(statement)
        bom_items = result.all()

        items = [
            BomModelResponse(
                id=bom_item.id,
                product_id=bom_item.product.id if bom_item.product else None,
                product_code=(
                    bom_item.product.product_code if bom_item.product else None
                ),
                material_id=bom_item.material.id if bom_item.material else None,
                material_code=(
                    bom_item.material.material_code if bom_item.material else None
                ),
            )
            for bom_item in bom_items
        ] or []

        return Page.create(total=len(bom_items), items=items, params=params)

    async def get_bom_item(self, bom_id: str, session: AsyncSession):
        try:
            bom_uuid = UUID(bom_id)
        except ValueError:
            raise InvalidIDFormat()

        bom = await session.get(BillOfMaterial, bom_uuid)
        if bom is None:
            raise None
        return bom

    async def get_bom_from_product_id(self, product_id: str, session: AsyncSession):
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise InvalidIDFormat()

        statement = (
            select(BillOfMaterial)
            .where(BillOfMaterial.product_id == product_uuid)
            .options(
                selectinload(BillOfMaterial.product),
                selectinload(BillOfMaterial.material),
            )
        )
        result = await session.exec(statement)
        bom_items = result.all()

        if not bom_items:
            return None

        data_response = [
            BomDetailModelResponse(
                id=bom.id,
                product_id=bom.product_id,
                material_id=bom.material_id,
                quantity_per_product=bom.quantity_per_product,
                unit_per_product=bom.unit_per_product,
                product_code=bom.product.product_code,
                product_name=bom.product.name,
                material_code=bom.material.material_code,
                material_name=bom.material.name,
            )
            for bom in bom_items
        ]
        return data_response

    async def create_bom_item(self, bom_data: CreateBomModel, session: AsyncSession):
        existing_product = await session.get(Product, bom_data.product_id)
        if existing_product is None:
            raise ProductNotFound()

        existing_material = await session.get(Material, bom_data.material_id)
        if existing_material is None:
            raise MaterialNotFound()

        data_dict = bom_data.model_dump()
        new_bom = BillOfMaterial(**data_dict)
        session.add(new_bom)
        await session.commit()
        return new_bom

    async def update_bom(
        self, bom_id: str, data_update: CreateBomModel, session: AsyncSession
    ):
        try:
            bom_uuid = UUID(bom_id)
        except ValueError:
            raise InvalidIDFormat()

        bom_to_update = await self.get_bom_item(bom_id, session)

        if bom_to_update is None:
            raise BomNotFound()

        product = await session.get(Product, data_update.product_id)
        if product is None:
            raise ProductNotFound()

        material = await session.get(Material, data_update.material_id)
        if material is None:
            raise MaterialNotFound()

        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(bom_to_update, key, value)
        await session.commit()
        return bom_to_update

    async def delete_bom(self, bom_id: str, session: AsyncSession):
        try:
            bom_uuid = UUID(bom_id)
        except ValueError:
            raise InvalidIDFormat()

        bom_to_delete = await self.get_bom_item(bom_id, session)
        if bom_to_delete is not None:
            await session.delete(bom_to_delete)
            await session.commit()
            return bom_to_delete
        return None
