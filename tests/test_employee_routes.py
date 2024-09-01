import os
import unittest
from unittest.mock import patch

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from fastapi_demo.db.db_session import _get_engine, get_session
from fastapi_demo.models.designation import Designation
from fastapi_demo.models.employee import Employee
from fastapi_demo.routes.employee import emp
from fastapi_demo.utils.utility import MissingEmployeeRecord


class EmployeeRouteTest(unittest.TestCase):
    def setUp(self):
        load_dotenv("test.env")
        self.engine = _get_engine()
        SQLModel.metadata.create_all(self.engine)
        self.session = get_session()
        self.client = TestClient(emp)

        # Create a sample designation for testing
        self.designation = Designation(name="Software Engineer")
        with Session(self.engine) as session:
            session.add(self.designation)
            session.commit()
            session.refresh(self.designation)

    def tearDown(self):
        load_dotenv()
        os.remove("test_db")  # Ensure this points to the correct test DB path
        self.session.close()
        self.engine.dispose()

    @patch("fastapi_demo.db.db_session.get_session")
    def test_create_employee(self, mock_get_session):
        mock_get_session.return_value = self.session
        employee_data = {
            "name": "Test Employee",
            "designation_id": str(
                self.designation.id
            ),  # Convert UUID to string
        }
        response = self.client.post("/employee", json=employee_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], employee_data["name"])
        self.assertEqual(
            response.json()["designation_id"], str(self.designation.id)
        )  # Compare with string

    @patch("fastapi_demo.db.db_session.get_session")
    def test_get_employee(self, mock_get_session):
        mock_get_session.return_value = self.session
        employee = Employee(
            name="Test Employee", designation_id=self.designation.id
        )
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        response = self.client.get(f"/employee/{employee.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Employee")
        self.assertEqual(
            response.json()["designation_id"], str(self.designation.id)
        )

    @patch("fastapi_demo.db.db_session.get_session")
    def test_get_employees(self, mock_get_session):
        mock_get_session.return_value = self.session
        employee1 = Employee(
            name="Test Employee 1", designation_id=self.designation.id
        )
        employee2 = Employee(
            name="Test Employee 2", designation_id=self.designation.id
        )
        self.session.add_all([employee1, employee2])
        self.session.commit()
        response = self.client.get("/employee")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["name"], "Test Employee 1")
        self.assertEqual(
            response.json()[0]["designation_id"], str(self.designation.id)
        )
        self.assertEqual(response.json()[1]["name"], "Test Employee 2")
        self.assertEqual(
            response.json()[1]["designation_id"], str(self.designation.id)
        )

    @patch("fastapi_demo.db.db_session.get_session")
    def test_delete_employee(self, mock_get_session):
        mock_get_session.return_value = self.session
        employee = Employee(
            name="Test Employee", designation_id=self.designation.id
        )
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        response = self.client.delete(f"/employee/{employee.id}")
        self.assertEqual(response.status_code, 204)

    @patch("fastapi_demo.db.db_session.get_session")
    def test_get_employee_not_found(self, mock_get_session):
        mock_get_session.return_value = self.session
        with self.assertRaises(MissingEmployeeRecord) as context:
            self.client.get("/employee/123e4567-e89b-12d3-a456-426614174000")
            self.assertEqual(
                context.exception.detail, "Missing employee record."
            )

    @patch("fastapi_demo.db.db_session.get_session")
    def test_update_employee(self, mock_get_session):
        mock_get_session.return_value = self.session
        employee = Employee(
            name="Test Employee", designation_id=self.designation.id
        )
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        update_data = {
            "name": "Updated Test Employee",
            "designation_id": str(self.designation.id),  # Convert to string
        }
        response = self.client.patch(
            f"/employee/{employee.id}", json=update_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Test Employee")
        self.assertEqual(
            response.json()["designation_id"], str(self.designation.id)
        )

    @patch("fastapi_demo.db.db_session.get_session")
    def test_update_employee_not_found(self, mock_get_session):
        update_data = {
            "name": "Updated Test Employee",
            "designation_id": str(self.designation.id),  # Convert to string
        }
        with self.assertRaises(MissingEmployeeRecord) as context:
            response = self.client.patch(
                "/employee/123e4567-e89b-12d3-a456-426614174000",
                json=update_data,
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                context.exception.detail, "Missing employee record."
            )


if __name__ == "__main__":
    unittest.main()
