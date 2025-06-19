from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from fastapi_pagination.ext.sqlmodel import apaginate
from fastapi_pagination import Page

from app.db.model import Material, BillOfMaterial
from app.material.schema import (
    CreateMaterialModel,
    BillOfMaterialBase,
    MaterialDetailResponse,
)
from app.error import InvalidIDFormat, MaterialNotFound, MaterialAlreadyExist


class MaterialService:
    async def get_all_material(self, session: AsyncSession) -> Page[Material]:
        statement = select(Material).order_by(Material.name)
        return await apaginate(session, statement)

    async def get_material_item(self, material_id: str, session: AsyncSession):
        try:
            material_uuid = UUID(material_id)
        except ValueError:
            raise InvalidIDFormat()

        statement = (
            select(Material)
            .where(Material.id == material_uuid)
            .options(
                selectinload(Material.inventory),
                selectinload(Material.bill_of_materials).selectinload(
                    BillOfMaterial.product
                ),
            )
        )
        result = await session.exec(statement)
        material_detail = result.first()

        if material_detail is None:
            raise MaterialNotFound()

        # Process bill of materials safely - using the correct attribute name
        bill_of_materials = []
        if material_detail.bill_of_materials:
            bill_of_materials = [
                BillOfMaterialBase(
                    product_code=bom.product.product_code,
                    product_name=bom.product.name,
                )
                for bom in material_detail.bill_of_materials
                if bom and bom.product
            ] or []

        response_data = {
            **material_detail.model_dump(),
            "quantity_in_stock": (
                material_detail.inventory.quantity if material_detail.inventory else 0.0
            ),
            "bill_of_materials": bill_of_materials,
        }

        return MaterialDetailResponse(**response_data)

    async def create_material(
        self, material_data: CreateMaterialModel, session: AsyncSession
    ):
        statement = select(Material).where(
            Material.material_code == material_data.material_code
        )
        result = await session.exec(statement)
        existing_material = result.first()
        if existing_material:
            raise MaterialAlreadyExist()

        data_dict = material_data.model_dump()
        new_material = Material(**data_dict)
        session.add(new_material)
        await session.commit()
        return new_material

    async def update_material(
        self, material_id: str, data_update: CreateMaterialModel, session: AsyncSession
    ):
        try:
            material_uuid = UUID(material_id)
        except ValueError:
            raise InvalidIDFormat()

        material_to_update = await session.get(Material, material_uuid)

        if material_to_update is None:
            return None

        if material_to_update.material_code != data_update.material_code:
            statement = select(Material).where(
                Material.material_code == data_update.material_code
            )
            result = await session.exec(statement)
            existing_material = result.first()
            if existing_material:
                raise MaterialAlreadyExist()
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(material_to_update, key, value)
        await session.commit()

        return material_to_update

    async def delete_material(self, material_id: str, session: AsyncSession):
        try:
            material_uuid = UUID(material_id)
        except ValueError:
            raise InvalidIDFormat()
        material_to_delete = await session.get(Material, material_uuid)
        if material_to_delete is not None:
            await session.delete(material_to_delete)
            await session.commit()
            return material_to_delete
        return None
