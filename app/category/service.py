from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


from app.category.schema import CreateCategoryModel
from app.db.model import Category
from app.error import CategoryAlreadyExist


class CategoryService:
    async def get_all_category(self, session: AsyncSession):
        statement = select(Category).order_by(Category.name)
        results = await session.exec(statement)
        categories = results.all()
        return categories

    async def get_category_item(self, category_id: str, session: AsyncSession):
        category_uuid = UUID(category_id)
        statement = select(Category).where(Category.id == category_uuid)
        results = await session.exec(statement)
        category_item = results.first()
        return category_item

    async def create_category(
        self, category_data: CreateCategoryModel, session: AsyncSession
    ):
        data_dict = category_data.model_dump()
        # Exists checking
        category_exist = (
            await session.exec(
                select(Category).where(Category.name == data_dict["name"])
            )
        ).first()
        if category_exist is not None:
            raise CategoryAlreadyExist()

        new_category = Category(**data_dict)
        session.add(new_category)
        await session.commit()
        return new_category

    async def update_category(
        self, category_id: str, data_update: CreateCategoryModel, session: AsyncSession
    ):
        category_exits = (await session.exec(select(Category).where(Category.name == data_update.name))).first()
        if category_exits is not None:
            raise CategoryAlreadyExist()

        category_to_update = await self.get_category_item(category_id, session)

        if category_to_update is not None:
            data_dict = data_update.model_dump()

            for key, value in data_dict.items():
                setattr(category_to_update, key, value)

            await session.commit()
            return category_to_update
        else:
            return None

    async def delete_category(self, category_id: str, session: AsyncSession):
        category_to_delete = await self.get_category_item(category_id, session)
        if category_to_delete is not None:
            await session.delete(category_to_delete)
            await session.commit()
            return category_to_delete
        return None
