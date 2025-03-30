from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.model import Material
from app.material.schema import CreateMaterialModel


class MaterialService:
    async def get_all_material(self, session: AsyncSession):
        statement = select(Material).order_by(Material.name)
        results = await session.exec(statement)
        materials = results.all()
        return materials

    async def get_material_item(self, material_id: str, session: AsyncSession):
        statement = select(Material).where(Material.id == material_id)
        result = await session.exec(statement)
        material = result.first()
        return material

    async def create_material(self, material_data: CreateMaterialModel, session: AsyncSession):
        data_dict = material_data.model_dump()
        new_material = Material(**data_dict)
        session.add(new_material)
        await session.commit()
        return new_material

    async def update_material(self, material_id: str, data_update: CreateMaterialModel, session: AsyncSession):
        material_to_update = await self.get_material_item(material_id, session)
        if material_to_update is not None:
            data_dict = data_update.model_dump()
            for key, value in data_dict.items():
                setattr(material_to_update, key, value)
            await session.commit()
            return material_to_update
        return None

    async def delte_material(self, material_id: str, session: AsyncSession):
        material_to_delete = await self.get_material_item(material_id, session)
        if material_to_delete is not None:
            await session.delete(material_to_delete)
            await session.commit()
            return material_to_delete
        return None