import os
import unittest
import uuid
from unittest.mock import patch

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from fastapi_demo.db.db_session import _get_engine, get_session
from fastapi_demo.models.designation import Designation
from fastapi_demo.routes.designation import designation_router

client = TestClient(designation_router)


class TestDesignationRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up testing environment."""
        load_dotenv("test.env")
        cls.engine = _get_engine()
        SQLModel.metadata.create_all(cls.engine)
        cls.session = get_session()

    @classmethod
    def tearDownClass(cls):
        """Clean up after testing."""
        load_dotenv()
        os.remove("test_db")
        cls.session.close()
        cls.engine.dispose()

    def test_create_department_route_success(self):
        """Test successful department creation."""
        with patch(
            "fastapi_demo.data.designation.create_designation"
        ) as mock_create_designation, patch(
            "fastapi_demo.routes.designation.get_session",
            return_value=self.session,
        ):
            designation_data = {"name": "Test Designation"}
            mock_create_designation.return_value = Designation(
                id=uuid.uuid4(), **designation_data
            )

            response = client.post("/designations/", json=designation_data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["name"], "Test Designation")

    def test_create_department_route_value_error(self):
        """Test handling of a ValueError during department creation."""
        with patch(
            "fastapi_demo.data.designation.create_designation"
        ) as mock_create_designation, patch(
            "fastapi_demo.routes.designation.get_session",
            return_value=self.session,
        ):
            mock_create_designation.side_effect = ValueError(
                "Department with this name already exists."
            )
            response = client.post(
                "/designations/", json={"name": "Test Designation"}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(),
                {"message": "Department with this name already exists."},
            )

    def test_delete_designation_route_success(self):
        """Test successful deletion of a designation."""
        with patch(
            "fastapi_demo.data.designation.delete_designation"
        ) as mock_delete_designation, patch(
            "fastapi_demo.routes.designation.get_session",
            return_value=self.session,
        ):
            mock_delete_designation.return_value = True
            response = client.delete(f"/designations/{uuid.uuid4()}")

            self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
