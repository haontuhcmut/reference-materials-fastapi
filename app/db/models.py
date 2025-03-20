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

    sample_deliveries: list["SampleDelivery"] = Relationship(back_populates="sample")
    status_reports: list["StatusReport"] = Relationship(back_populates="sample")
    dhs: list["Dh"] = Relationship(back_populates="sample")

class SampleDelivery(SQLModel, table=True):
    __tablename__ = "sample_delivery"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sample_id: uuid.UUID | None = Field(default=None, foreign_key="sample.id")
    created_at: date
    delivery_date: date
    description: str | None = Field(default=None, max_length=1024)

    sample: Sample | None = Relationship(back_populates="sample_deliveries")
    status_reports: list["StatusReport"] = Relationship(back_populates="sample_delivery")


class Dh(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    code: str = Field(default=None, min_length=1, max_length=15, nullable=False, unique=True)
    sample_id: uuid.UUID | None = Field(default=None, foreign_key="sample.id")

    sample: Sample | None = Relationship(back_populates="dhs")
    status_report: Optional["StatusReport"] = Relationship(back_populates="dh")


class StatusReport(SQLModel, table=True):
    __tablename__ = "status_report"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sample_id: uuid.UUID | None = Field(default=None, foreign_key="sample.id")
    sample_delivery_id: uuid.UUID | None = Field(default=None, foreign_key="sample_delivery.id")
    dh_id: uuid.UUID | None = Field(default=None, foreign_key="dh.id")
    status: str = Field(default=None, min_length=1, nullable=False)
    description: str | None = Field(default=None, min_length=1, max_length=1024)

    sample: Sample | None = Relationship(back_populates="status_reports")
    sample_delivery: SampleDelivery | None = Relationship(back_populates="status_reports")
    dh: Dh | None = Relationship(back_populates="status_report")






