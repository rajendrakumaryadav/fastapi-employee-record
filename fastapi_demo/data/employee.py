from uuid import UUID

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..models.employee import Employee, EmployeeRead, EmployeeUpdate


def get_employees(session: Session):
    try:
        employees = session.exec(select(Employee)).fetchall()
        employee_list = [
            EmployeeRead.model_validate(employee) for employee in employees
        ]
        return employee_list
    except Exception as e:
        print(e)
        return []


def get_employee(session: Session, id: UUID):
    try:
        employee = session.get_one(Employee, id)
        return employee
    except sqlalchemy.exc.NoResultFound:
        return None


def create_employee_record(session: Session, employee: Employee):
    try:
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return EmployeeRead.model_validate(employee)
    except IntegrityError as ex:
        return ex
    except Exception as ex:
        return ex


def delete_employee(session: Session, id: UUID):
    employee = get_employee(session, id=id)
    if employee is not None:
        session.delete(employee)
        session.commit()
        return True
    return None


def update_employee(session: Session, employee: EmployeeUpdate, id: UUID):
    db_employee = session.get(Employee, id)

    if db_employee is None:
        return None

    employee_data = employee.model_dump(exclude_unset=True)

    for key, value in employee_data.items():
        setattr(db_employee, key, value)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)

    return db_employee
