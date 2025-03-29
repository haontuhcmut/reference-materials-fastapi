from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.model import PTScheme
from app.pt_scheme.schema import CreatePTSchemeModel


class PTSchemeService:
    async def get_all_scheme(self, session: AsyncSession):
        statement = select(PTScheme).order_by(PTScheme.name)
        results = await session.exec(statement)
        schemes = results.all()
        return schemes

    async def get_scheme_item(self, scheme_id: str, session: AsyncSession):
        scheme_uuid = UUID(scheme_id)
        statement = select(PTScheme).where(PTScheme.id == scheme_uuid)
        result = await session.exec(statement)
        scheme = result.first()
        return scheme

    async def create_scheme(self, scheme_data: CreatePTSchemeModel, session: AsyncSession):
        data_dict = scheme_data.model_dump()
        new_scheme = PTScheme(**data_dict)
        session.add(new_scheme)
        await session.commit()
        return new_scheme

    async def update_scheme(self, scheme_id: str, data_update: CreatePTSchemeModel, session: AsyncSession):
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
