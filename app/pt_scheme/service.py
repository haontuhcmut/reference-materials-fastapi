from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload


from app.db.model import PTScheme, Category
from app.pt_scheme.schema import CreatePTSchemeModel, PTSchemeWithCategoryModel
from app.error import PTSchemeAlreadyExist, InvalidIDFormat
from app.utility.main import check_fk_exists

class PTSchemeService:

    async def get_all_pt_scheme(self, session: AsyncSession):
        statement = (
            select(PTScheme)
            .options(selectinload(PTScheme.category))  # Eager load category
            .order_by(PTScheme.pt_scheme_code)
        )

        result = await session.exec(statement)
        pt_schemes = result.all()
        data_response = [
            PTSchemeWithCategoryModel(
                **scheme.model_dump(),
                category_name=scheme.category.name if scheme.category else None
            )
            for scheme in pt_schemes
        ]
        return data_response

    async def get_scheme_item(self, scheme_id: str, session: AsyncSession):
        try:
            scheme_uuid = UUID(scheme_id)
        except ValueError:
            raise InvalidIDFormat()

        statement = (
            select(PTScheme, Category.name.label("category_name"))
            .join(Category, PTScheme.category_id == Category.id)
            .where(PTScheme.id == scheme_uuid)
        )
        result = await session.exec(statement)
        row = result.first()
        if row is None:
            return None
        scheme, category_name = row
        return scheme, category_name

    async def create_scheme(
        self, scheme_data: CreatePTSchemeModel, session: AsyncSession
    ):
        category = await check_fk_exists(
            model=Category,
            id_value=scheme_data.category_id,
            field_name="Category",
            session=session
        )

        statement = select(PTScheme).where(PTScheme.pt_scheme_code == scheme_data.pt_scheme_code)
        result = await session.exec(statement)
        scheme = result.first()
        if scheme is not None:
            raise PTSchemeAlreadyExist()

        data_dict = scheme_data.model_dump()
        new_scheme = PTScheme(**data_dict)
        session.add(new_scheme)
        await session.commit()
        return new_scheme, category.name

    async def update_scheme(
        self, scheme_id: str, data_update: CreatePTSchemeModel, session: AsyncSession
    ):
        try:
            scheme_uuid = UUID(scheme_id)
        except ValueError:
            raise InvalidIDFormat()

        scheme = await check_fk_exists(PTScheme, scheme_uuid, "PT scheme", session)
        category = await check_fk_exists(Category, data_update.category_id, "Category", session)

        if scheme.pt_scheme_code != data_update.pt_scheme_code:
            existing_scheme = (
                await session.exec(
                    select(PTScheme)
                    .where(
                        PTScheme.pt_scheme_code == data_update.pt_scheme_code,
                        PTScheme.id != scheme_uuid
                    )
                )
            ).first()
            if existing_scheme:
                raise PTSchemeAlreadyExist()
        for key, value in data_update.model_dump(exclude_unset=True).items():
            setattr(scheme, key, value)

        await session.commit()
        return scheme, category.name


    async def delete_scheme(self, scheme_id: str, session: AsyncSession):
        try:
            scheme_uuid = UUID(scheme_id)
        except ValueError:
            raise InvalidIDFormat()

        scheme_to_delete = await session.get(PTScheme, scheme_uuid)
        if scheme_to_delete is not None:
            await session.delete(scheme_to_delete)
            await session.commit()
            return scheme_to_delete
        return None
