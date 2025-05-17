from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from fastapi_pagination import Page, paginate

from app.db.model import PTScheme, Category
from app.pt_scheme.schema import CreatePTSchemeModel, PTSchemeWithCategoryModel


class PTSchemeService:
    async def get_all_pt_scheme(
        self, session: AsyncSession
    ) -> Page[PTSchemeWithCategoryModel]:
        query = (
            select(PTScheme)
            .options(selectinload(PTScheme.category))  # Eager load category
            .order_by(PTScheme.name)
        )

        result = await session.exec(query)
        pt_schemes = result.all()

        schemes = [
            PTSchemeWithCategoryModel(
                id=scheme.id,
                pt_name=scheme.name,
                year=scheme.year,
                analytes=scheme.analytes,
                category_name=scheme.category.name,  # Access through relationship
            )
            for scheme in pt_schemes
        ]

        return paginate(schemes)

    async def get_scheme_item(self, scheme_id: str, session: AsyncSession):
        scheme_uuid = UUID(scheme_id)
        statement = (select(PTScheme, Category.name.label("category_name"))
                     .join(Category, PTScheme.category_id == Category.id)
                     .where(PTScheme.id == scheme_uuid)
                     )
        result = await session.exec(statement)
        row = result.first()
        if row is None:
            return None
        scheme, category_name =row
        scheme_dict = scheme.model_dump()
        return PTSchemeWithCategoryModel(
            **scheme_dict,
            category_name= category_name
        )

    async def create_scheme(
        self, scheme_data: CreatePTSchemeModel, session: AsyncSession
    ):
        data_dict = scheme_data.model_dump()
        new_scheme = PTScheme(**data_dict)
        session.add(new_scheme)
        await session.commit()
        return new_scheme

    async def update_scheme(
        self, scheme_id: str, data_update: CreatePTSchemeModel, session: AsyncSession
    ):
        scheme_to_update = await self.get_scheme_item(scheme_id, session)
        if scheme_to_update is not None:
            data_dict = data_update.model_dump()
            for key, value in data_dict.items():
                setattr(scheme_to_update, key, value)
            await session.commit()
            return scheme_to_update
        return None

    async def delete_scheme(self, scheme_id: str, session: AsyncSession):
        scheme_to_delete = await self.get_scheme_item(scheme_id, session)
        if scheme_to_delete is not None:
            await session.delete(scheme_to_delete)
            await session.commit()
            return scheme_to_delete
        return None
