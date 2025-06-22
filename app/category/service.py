from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi_pagination.ext.sqlmodel import apaginate
from fastapi_pagination import Page, Params
from fastapi import Depends

from app.category.schema import CreateCategoryModel, CategoryFilter
from app.db.model import Category, PTScheme
from app.error import CategoryAlreadyExist, InvalidIDFormat, CategoryNotFound

from fastapi_filter import FilterDepends
from typing import Annotated


class CategoryService:
    async def get_all_category(self, session: AsyncSession) -> Page[Category]:
        statement = select(Category).order_by(Category.name)
        return await apaginate(session, statement)

    async def get_category_item(self, category_id: str, session: AsyncSession):
        try:
            category_uuid = UUID(category_id)
        except ValueError:
            raise InvalidIDFormat()

        category_item = await session.get(Category, category_uuid)
        if category_item is None:
            raise CategoryNotFound()
        return category_item

    async def create_category(
        self, category_data: CreateCategoryModel, session: AsyncSession
    ):
        data_dict = category_data.model_dump()
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
        try:
            category_uuid = UUID(category_id)
        except ValueError:
            raise InvalidIDFormat()

        category = await session.get(Category, category_uuid)
        if category is None:
            return None

        if data_update.name != category.name:
            existing_category = (
                await session.exec(
                    select(Category).where(
                        Category.name == data_update.name, Category.id != category_uuid
                    ),
                )
            ).first()
            if existing_category:
                raise CategoryAlreadyExist()

        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        await session.commit()
        return category

    async def delete_category(self, category_id: str, session: AsyncSession):
        category_to_delete = await self.get_category_item(category_id, session)
        if category_to_delete is not None:
            await session.delete(category_to_delete)
            await session.commit()
            return category_to_delete
        return None

    async def category_filter(
        self,
        category_filter: Annotated[CategoryFilter, FilterDepends(CategoryFilter)],
        session: AsyncSession,
        _params: Annotated[Params, Depends()],
    ) -> Page[Category]:
        statement = select(Category)
        filtered_query = category_filter.filter(statement)
        sorted_query = category_filter.sort(filtered_query)
        return await apaginate(session, sorted_query, _params)
