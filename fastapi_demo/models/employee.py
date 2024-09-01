import uuid
from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from fastapi_demo.models.designation import DesignationRead


class EmployeeBase(SQLModel):
    name: str = Field(nullable=False, max_length=200, min_length=3)
    joining_date: date = Field(default=date.today(), nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=True)


class Employee(EmployeeBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True
    )
    designation_id: Optional[uuid.UUID] = Field(
        foreign_key="designation.id", nullable=True, default=None
    )
    designation: Optional["Designation"] = Relationship(
        back_populates="employees"
    )


class EmployeeCreate(EmployeeBase):
    designation_id: uuid.UUID


class EmployeeRead(EmployeeBase):
    id: Optional[uuid.UUID]
    designation: Optional[DesignationRead]
    designation_id: Optional[uuid.UUID]


class EmployeeUpdate(SQLModel):
    name: Optional[str] = Field(nullable=True, max_length=200, min_length=3)
    designation_id: uuid.UUID | None = Field(nullable=True, default=None)
