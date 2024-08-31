from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from fastapi_demo.data.employee import (
    create_employee_record,
    delete_employee,
    get_employee,
    get_employees,
    update_employee,
)
from fastapi_demo.models.employee import (
    Employee,
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
)

from ..db.db_session import get_session
from ..models.exception import Message
from ..utils.utility import MissingEmployeeRecord

emp = APIRouter(
    tags=["employee"],
    prefix="/employee",
    responses={404: {"model": Message}},
)


@emp.post(
    "/",
    response_model=EmployeeRead,
    description="Create a new employee record.",
)
async def create_employee(
    *, session: Session = Depends(get_session), employee: EmployeeCreate
):
    db_employee = Employee.model_validate(employee)
    employee_res = create_employee_record(session=session, employee=db_employee)
    if not employee_res:
        raise HTTPException(
            status_code=500,
            detail="Duplicate entry or something went wrong on server.",
        )
    return employee_res


@emp.get("/{id}", response_model=EmployeeRead)
async def employee(*, session: Session = Depends(get_session), id: UUID):
    employee = get_employee(session, id=id)
    if not employee:
        raise MissingEmployeeRecord(
            status_code=404, detail="Missing employee record."
        )
        return
    return employee


@emp.get("/", response_model=List[EmployeeRead])
async def employees(*, session: Session = Depends(get_session)):
    return get_employees(session=session)


@emp.delete(
    "/{id}",
    description="Delete the model if exists",
    response_model=None,
    status_code=204,
)
async def delete(
    *, session: Session = Depends(get_session), id: UUID, response: Response
):
    deleted_status = delete_employee(session=session, id=id)
    if deleted_status:
        response.status_code = 204
        return None
    else:
        response.status_code = 404
        raise MissingEmployeeRecord(
            status_code=404, detail="Missing employee record."
        )
        # return None


@emp.patch(
    "/{id}",
    description="Update the existing record if exists.",
    response_model=Employee,
)
async def update(
    *,
    session: Session = Depends(get_session),
    id: UUID,
    employee: EmployeeUpdate,
):
    updated_employee = update_employee(
        session=session, employee=employee, id=id
    )

    if updated_employee is None:
        raise MissingEmployeeRecord(
            status_code=404, detail="Missing employee record."
        )
        return

    return updated_employee
