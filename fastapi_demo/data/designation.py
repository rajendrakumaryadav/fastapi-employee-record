from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select, text

from fastapi_demo.utils.utility import MissingEmployeeRecord

from ..models.designation import Designation, DesignationCreate


def create_designation(session: Session, department: DesignationCreate):
    department_db = Designation.model_validate(department)
    try:
        session.add(department_db)
        session.commit()
        session.refresh(department_db)
        return department_db
    except IntegrityError:
        raise ValueError("Department with this name already exists.")


def get_designation(session: Session):
    designations = session.exec(select(Designation)).all()
    return designations


def delete_designation(session: Session, id: str):
    try:
        # Directly attempt to delete the designation
        stmt = text("DELETE FROM designation WHERE id = :id")
        session.execute(stmt, {"id": str(id)})
        session.commit()
        return True  # Successful deletion

    except NoResultFound:
        # If no row is found to delete, it means the designation doesn't exist
        raise MissingEmployeeRecord(
            status_code=404, detail="Designation not found."
        )

    except Exception as ex:
        # Handle any other potential exceptions during the deletion process
        session.rollback()
        print(ex)
        return False
