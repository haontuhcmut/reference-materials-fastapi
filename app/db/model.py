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
    item_type_id: UUID | None = Field(default=None, foreign_key="item_type.id")
    pt_scheme_id: UUID | None = Field(default=None, foreign_key="pt_scheme.id")
    product_code: str = Field(default=None, max_length=32, nullable=False, unique=True)
    name: str = Field(default=None, max_length=128)
    sku: str = Field(default=None, max_length=128, unique=True)
    status: str | None = Field(default=None, max_length=16)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    item_type: Optional["ItemType"] = Relationship(back_populates="products")
    pt_scheme: PTScheme | None = Relationship(back_populates="products")
    bill_of_materials: list["BillOfMaterial"] = Relationship(back_populates="product")


class BillOfMaterial(SQLModel, table=True):
    __tablename__ = "bill_of_material"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID | None = Field(default=None, foreign_key="product.id")
    material_id: UUID | None = Field(default=None, foreign_key="material.id")
    quantity_required: int = Field(default=0, ge=0, le=999)

    product: Optional[Product] = Relationship(back_populates="bill_of_materials")
    material: Optional["Material"] = Relationship(back_populates="bill_of_materials")


class Material(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID | None = Field(default=None, foreign_key="item_type.id")
    material_code: str = Field(default=None, max_length=32, nullable=False, unique=True)
    name: str = Field(default=None, max_length=128, nullable=False)
    detailed_info: str | None = Field(default=None, max_length=1028)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    bill_of_materials: list[BillOfMaterial] = Relationship(back_populates="material")
    item_type: Optional["ItemType"] = Relationship(back_populates="materials")


class ItemType(SQLModel, table=True):
    __tablename__ = "item_type"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_type_code: str = Field(default=None, max_length=32, unique=True)
    name: str = Field(default=None, max_length=32)
    item_type: str = Field(default=None,  max_length=128)
    unit: str = Field(default=None, max_length=16)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    products: list[Product] = Relationship(back_populates="item_type")
    materials: list[Material] = Relationship(back_populates="item_type")
    transactions: list["Transaction"] = Relationship(back_populates="item_type")
    inventories: list["Inventory"] = Relationship(back_populates="item_type")
    testing_plans: list["TestingPlan"] = Relationship(back_populates="item_type")

class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    warehouse_id: UUID | None = Field(default=None, foreign_key="warehouse.id")
    item_type_id: UUID | None = Field(default=None, foreign_key="item_type.id")
    transaction_type: str = Field(default=None, max_length=64)
    quantity: float = Field(default=0, ge=0, le=99999)
    description: str = Field(default=None, max_length=1024)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    warehouse: Optional["Warehouse"] = Relationship(back_populates="transactions")
    item_type: ItemType | None = Relationship(back_populates="transactions")


class Warehouse(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(default=None, max_length=128, nullable=False)
    location: str = Field(default=None, max_length=128, nullable=False)
    type: str = Field(default=None, max_length=32)

    transactions: list[Transaction] = Relationship(back_populates="warehouse")
    inventories: list["Inventory"] = Relationship(back_populates="warehouses")


class Inventory(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    warehouse_id: UUID | None = Field(default=None, foreign_key="warehouse.id")
    item_type_id: UUID | None = Field(default=None, foreign_key="item_type.id")
    quantity: float = Field(default=0, ge=0, le=99999)
    last_update: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    warehouses: Warehouse | None = Relationship(back_populates="inventories")
    item_type: ItemType | None = Relationship(back_populates="inventories")


class TestingPlan(SQLModel, table=True):
    __tablename__ = "testing_plan"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_type_id: UUID | None = Field(default=None, foreign_key="item_type.id")
    quantity: int = Field(default=0, ge=0, le=999)
    unit: str | None = Field(default=None, max_length=16)
    sending_date: date
    delivery_date: date
    description: str | None = Field(default=None, max_length=1024)

    item_type: ItemType | None = Relationship(back_populates="testing_plans")
    internal_contract: Optional["InternalContract"] = Relationship(
        back_populates="testing_plan"
    )


class InternalContract(SQLModel, table=True):
    __tablename__ = "internal_contract"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    testing_plan_id: UUID | None = Field(default=None, foreign_key="testing_plan.id")
    contract_id: str = Field(default=None, max_length=16)
    expected_date_results: date
    created_at: date

    testing_plan: TestingPlan | None = Relationship(back_populates="internal_contract")
