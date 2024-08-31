import uuid
from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class EmployeeBase(SQLModel):
    name: str = Field(nullable=False, max_length=200, min_length=3)
    designation: str = Field(nullable=False, max_length=200, min_length=3)
    joining_date: date = Field(default=date.today(), nullable=True)
    created_at: datetime = Field(default=datetime.now(), nullable=True)


class Employee(EmployeeBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True
    )


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: uuid.UUID


class EmployeeUpdate(SQLModel):
    name: Optional[str] = Field(nullable=True, max_length=200, min_length=3)
    designation: Optional[str] = Field(
        nullable=True, max_length=200, min_length=3
    )
