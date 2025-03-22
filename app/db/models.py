import uuid
from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Sample(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sku: str = Field(default=None, max_length=15, min_length=1, nullable=False)
    name: str = Field(default=None, nullable=False)
    description: str = Field(default=None, max_length=1024, nullable=True)
    created_at: date

    delivery_plan: list["DeliveryPlan"] = Relationship(back_populates="sample")
    status_reports: list["StatusReport"] = Relationship(back_populates="sample")
    delivery: list["Delivery"] = Relationship(back_populates="sample")

class DeliveryPlan(SQLModel, table=True):
    __tablename__ = "delivery_plan"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sample_id: uuid.UUID | None = Field(default=None, foreign_key="sample.id")
    created_at: date
    delivery_date: date
    description: str | None = Field(default=None, max_length=1024)

    sample: Sample | None = Relationship(back_populates="delivery_plan")
    status_reports: list["StatusReport"] = Relationship(back_populates="delivery_plan")


class Delivery(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    delivery_code: str = Field(default=None, min_length=1, max_length=15, nullable=False, unique=True)
    sample_id: uuid.UUID | None = Field(default=None, foreign_key="sample.id")
    due_date: date
    created_at: date

    sample: Sample | None = Relationship(back_populates="delivery")
    status_report: Optional["StatusReport"] = Relationship(back_populates="delivery")


class StatusReport(SQLModel, table=True):
    __tablename__ = "status_report"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sample_id: uuid.UUID | None = Field(default=None, foreign_key="sample.id")
    delivery_plan_id: uuid.UUID | None = Field(default=None, foreign_key="delivery_plan.id")
    delivery_id: uuid.UUID | None = Field(default=None, foreign_key="delivery.id")
    status: str = Field(default=None, min_length=1, nullable=False)
    description: str | None = Field(default=None, min_length=1, max_length=1024)

    sample: Sample | None = Relationship(back_populates="status_reports")
    delivery_plan: DeliveryPlan | None = Relationship(back_populates="status_reports")
    delivery: Delivery | None = Relationship(back_populates="status_report")






