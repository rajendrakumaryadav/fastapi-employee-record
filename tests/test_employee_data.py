import os
import unittest
import uuid
from datetime import date, datetime
from unittest.mock import patch

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel

from fastapi_demo.db.db_session import _get_engine, get_session
from fastapi_demo.models.designation import Designation, DesignationRead
from fastapi_demo.models.employee import (
    Employee,
    EmployeeBase,
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
)


class EmployeeModelTest(unittest.TestCase):
    def setUp(self):
        load_dotenv("test.env")
        self.engine = _get_engine()
        SQLModel.metadata.create_all(self.engine)
        self.session = get_session()

        # Add a sample designation for the tests
        self.designation = Designation(name="Software Engineer")
        with Session(self.engine) as session:
            session.add(self.designation)
            session.commit()
            session.refresh(self.designation)

    def tearDown(self):
        load_dotenv()
        os.remove("test_db")
        self.session.close()
        self.engine.dispose()

    def test_employee_base_model_creation(self):
        employee_base = EmployeeBase(
            name="Test Employee",
            joining_date=date(2023, 10, 26),
        )
        self.assertEqual(employee_base.name, "Test Employee")
        self.assertEqual(employee_base.joining_date, date(2023, 10, 26))
        self.assertIsNotNone(employee_base.created_at)

    def test_employee_model_creation(self):
        employee = Employee(
            name="Test Employee",
            designation_id=self.designation.id,
            joining_date=date(2023, 10, 26),
        )
        self.assertEqual(employee.name, "Test Employee")
        self.assertEqual(employee.designation_id, self.designation.id)
        self.assertEqual(employee.joining_date, date(2023, 10, 26))
        self.assertIsNotNone(employee.created_at)
        self.assertIsNotNone(employee.id)

    def test_employee_create_model_creation(self):
        employee_create = EmployeeCreate(
            name="Test Employee",
            designation_id=self.designation.id,
        )
        self.assertEqual(employee_create.name, "Test Employee")
        self.assertEqual(employee_create.designation_id, self.designation.id)

    def test_employee_read_model_creation(self):
        employee_read = EmployeeRead(
            id=uuid.uuid4(),
            name="Test Employee",
            designation=DesignationRead(
                id=self.designation.id,  # This is correct
                name=self.designation.name,
            ),
            joining_date=date(2023, 10, 26),
            designation_id=self.designation.id,  # Add this line
        )
        self.assertEqual(employee_read.name, "Test Employee")
        self.assertEqual(employee_read.designation.id, self.designation.id)
        self.assertEqual(employee_read.joining_date, date(2023, 10, 26))
        self.assertIsNotNone(employee_read.id)
        self.assertEqual(employee_read.designation_id, self.designation.id)

    def test_employee_update_model_creation(self):
        employee_update = EmployeeUpdate(
            name="Updated Test Employee",
            designation_id=self.designation.id,
        )
        self.assertEqual(employee_update.name, "Updated Test Employee")
        self.assertEqual(employee_update.designation_id, self.designation.id)

    @patch("sqlmodel.Session")
    def test_employee_from_orm(self, mock_session):
        mock_session.return_value.execute.return_value.all.return_value = [
            {
                "id": uuid.uuid4(),
                "name": "Test Employee",
                "designation_id": self.designation.id,
                "joining_date": date(2023, 10, 26),
                "created_at": datetime.now(),
            }
        ]
        employee = Employee.model_validate(
            mock_session.return_value.execute.return_value.all.return_value[0]
        )
        self.assertEqual(employee.name, "Test Employee")
        self.assertEqual(employee.designation_id, self.designation.id)
        self.assertEqual(employee.joining_date, date(2023, 10, 26))
        self.assertIsNotNone(employee.id)


if __name__ == "__main__":
    unittest.main()
