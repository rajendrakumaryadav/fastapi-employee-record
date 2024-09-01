import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class DesignationBase(SQLModel):
    name: str = Field(unique=True, nullable=False)
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, nullable=True
    )


class Designation(DesignationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employees: List["Employee"] = Relationship(back_populates="designation")


class DesignationRead(DesignationBase):
    id: uuid.UUID


class DesignationCreate(DesignationBase):
    pass
