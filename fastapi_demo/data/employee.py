from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select, text

from fastapi_demo.utils.utility import MissingEmployeeRecord

from ..models.employee import (
    Employee,
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
)


def get_employees(session: Session):
    employees = session.exec(select(Employee)).all()
    employee_read_list = []
    for employee in employees:
        employee_read = EmployeeRead(
            id=employee.id,
            name=employee.name,
            joining_date=employee.joining_date,
            created_at=employee.created_at,
            designation_id=employee.designation_id,  # Include this line
            designation=employee.designation,
        )
        employee_read_list.append(employee_read)
    return employee_read_list


def get_employee(session: Session, id: UUID):
    try:
        employee = session.exec(select(Employee).where(Employee.id == id)).one()
        if not employee:
            raise MissingEmployeeRecord(
                status_code=404, detail="Missing employee record..."
            )
        employee_read = EmployeeRead(
            id=employee.id,
            name=employee.name,
            joining_date=employee.joining_date,
            created_at=employee.created_at,
            designation_id=employee.designation_id,
            designation=employee.designation,
        )

        return employee_read
    except NoResultFound:
        raise MissingEmployeeRecord(status_code=404, detail="Missing record.")


def create_employee_record(session: Session, employee: EmployeeCreate):
    try:
        db_employee = Employee.model_validate(employee)
        session.add(db_employee)
        session.commit()
        session.refresh(db_employee)
        return EmployeeRead.model_validate(db_employee)
    except IntegrityError as ex:
        session.rollback()
        print(ex)
        return None
    except Exception as ex:
        session.rollback()
        print(ex)
        return None


def update_employee(session: Session, employee: EmployeeUpdate, id: UUID):
    db_employee = session.get(Employee, id)
    if not db_employee:
        return None

    # Update fields if they are provided in the update request
    if employee.name is not None:
        db_employee.name = employee.name
    if employee.designation_id is not None:
        db_employee.designation_id = employee.designation_id

    # Add any other fields that need to be updated here

    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


def delete_employee(session: Session, id: UUID):
    employee = get_employee(session, id)

    if employee is not None:
        stmt = text("DELETE FROM employee WHERE id = :id")
        session.execute(stmt, {"id": str(id)})
        session.commit()
        return True
    else:
        raise MissingEmployeeRecord(
            status_code=404, detail="Missing employee record."
        )
