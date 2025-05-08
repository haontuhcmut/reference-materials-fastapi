from uuid import UUID, uuid4
from datetime import datetime, timezone, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(default=None, max_length=128, nullable=False, unique=True)

    pt_schemes: list["PTScheme"] = Relationship(back_populates="category")

class PTScheme(SQLModel, table=True):
    __tablename__ = "pt_scheme"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    category_id: UUID | None = Field(default=None, foreign_key="category.id")
    pt_scheme_code: str = Field(default=None, max_length=32, nullable=False, unique=True)
    name: str = Field(default=None, max_length=128, nullable=False)
    year: int | None = Field(default=None, ge=1900, le=2100)
    analytes: str | None = Field(default=None, max_length=128)

    category: Category | None = Relationship(back_populates="pt_schemes")
    products: list["Product"] = Relationship(back_populates="pt_scheme")


class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    pt_scheme_id: UUID | None = Field(default=None, foreign_key="pt_scheme.id")
    product_code: str = Field(default=None, max_length=32, nullable=False, unique=True)
    name: str = Field(default=None, max_length=128)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    pt_scheme: PTScheme | None = Relationship(back_populates="products")
    bill_of_materials: list["BillOfMaterial"] = Relationship(back_populates="product")
    transaction_details: list["TransactionDetail"] = Relationship(back_populates="product")
    inventory: Optional["Inventory"] = Relationship(back_populates="product")


class BillOfMaterial(SQLModel, table=True):
    __tablename__ = "bill_of_material"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID | None = Field(default=None, foreign_key="product.id")
    material_id: UUID | None = Field(default=None, foreign_key="material.id")

    product: Optional[Product] = Relationship(back_populates="bill_of_materials")
    material: Optional["Material"] = Relationship(back_populates="bill_of_materials")


class Material(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    material_code: str = Field(default=None, max_length=32, nullable=False, unique=True)
    name: str = Field(default=None, max_length=128, nullable=False)
    detailed_info: str | None = Field(default=None, max_length=1028)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    bill_of_materials: list[BillOfMaterial] = Relationship(back_populates="material")
    transaction_details: list["TransactionDetail"] = Relationship(back_populates="material")
    inventory: Optional["Inventory"] = Relationship(back_populates="material")


class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    transaction_type: str = Field(default=None, max_length=16)
    note: str | None = Field(default=None, max_length=1024)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    transaction_details: list["TransactionDetail"] = Relationship(back_populates="transaction")

class TransactionDetail(SQLModel, table=True):
    __tablename__ = "transaction_detail"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    transaction_id: UUID = Field(default=None, foreign_key="transaction.id")
    warehouse_id: UUID = Field(default=None, foreign_key="warehouse.id")
    product_id: UUID | None = Field(default=None, foreign_key="product.id")
    material_id: UUID | None = Field(default=None, foreign_key="material.id")
    quantity: float = Field(default=0, ge=0, le=99999)

    transaction: Transaction | None = Relationship(back_populates="transaction_details")
    warehouse: Optional["Warehouse"] = Relationship(back_populates="transaction_details")
    product: Product | None = Relationship(back_populates="transaction_details")
    material: Material | None = Relationship(back_populates="transaction_details")


class Warehouse(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(default=None, max_length=128, nullable=False)
    location: str = Field(default=None, max_length=128, nullable=False)
    type: str = Field(default=None, max_length=32)

    transaction_details: list[TransactionDetail] = Relationship(back_populates="warehouse")
    inventories: list["Inventory"] = Relationship(back_populates="warehouse")

class Inventory(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    warehouse_id: UUID = Field(default=None, foreign_key="warehouse.id")
    product_id: UUID | None = Field(default=None, foreign_key="product.id")
    material_id: UUID | None = Field(default=None, foreign_key="material.id")
    quantity: float = Field(default=0, ge=0, le=99999)
    last_update: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    product: Product | None = Relationship(back_populates="inventory")
    material: Material | None = Relationship(back_populates="inventory")
    warehouse: Warehouse | None = Relationship(back_populates="inventories")

