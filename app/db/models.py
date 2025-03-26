from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(default=None, max_length=128)

    pt_schemes: list["PTScheme"] = Relationship(back_populates="category")
class PTScheme(SQLModel, table=True):
    __tablename__ = "pt_scheme"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    category_id: UUID | None = Field(default=None, foreign_key="category.id")
    name: str = Field(default=None, max_length=128)
    year: int | None = Field(default=None, ge=1900, le=2100)
    analytes: str | None = Field(default=None, max_length=128)

    category: Category | None = Relationship(back_populates="pt_schemes")
    products: list["Product"] = Relationship(back_populates="pt_scheme")

class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_type_id: UUID | None = Field(default=None, foreign_key="item_type.id")
    pt_scheme_id: UUID | None = Field(default=None, foreign_key="pt_scheme.id")
    sku: str = Field(default=None, max_length=128, unique=True)
    quantity: int = Field(default=0, nullable=False, ge=0, le=999)
    unit: str | None = Field(default=None, max_length=16)
    status: str | None = Field(default=None, max_length=16)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    item_type: Optional["ItemType"] = Relationship(back_populates="products")
    pt_scheme: PTScheme | None = Relationship(back_populates="products")
    bill_of_materials: list["BillOfMaterial"] = Relationship(back_populates="product")

class BillOfMaterial(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID | None = Field(default=None, foreign_key="product.id")
    material_id: UUID | None = Field(default=None, foreign_key="material.id")
    quantity_required: int | None = Field(default=0, ge=0, le=999)

    product: Optional[Product] = Relationship(back_populates="bill_of_materials")
    material: Optional["Material"] = Relationship(back_populates="bill_of_materials")
class Material(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID | None = Field(default=None, foreign_key="item_type.id")
    internal_code: str = Field(default=None, nullable=False, unique=True)
    #name: str = Field(default=None)

    bill_of_materials: list[BillOfMaterial] = Relationship(back_populates="material")
    item_type: Optional["ItemType"] = Relationship(back_populates="materials")


class ItemType(SQLModel, table=True):
    __tablename__ = "item_type"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type_name: str = Field(default=None, max_length=128)

    products: list[Product] = Relationship(back_populates="item_type")
    materials: list[Material] = Relationship(back_populates="item_type")
