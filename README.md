[![Poetry-Pytest](https://github.com/rajendrakumaryadav/fastapi-employee-record/actions/workflows/poetry-pytest-test.yml/badge.svg)](https://github.com/rajendrakumaryadav/fastapi-employee-record/actions/workflows/poetry-pytest-test.yml)
### Primary Setup
1. Copy .env.example as .env
2. Update the username, password db and other option.
3. install the dependencies
```bash
$ poetry install
```
> Expecting poetry will be installed already.
4. Run the testcases
```bash
$ poetry run pytest -s -v

Output:

=========================================================== test session starts ============================================================
platform linux -- Python 3.12.4, pytest-8.3.2, pluggy-1.5.0 -- /home/username/.cache/pypoetry/virtualenvs/fastapi-demo-c0ss8YTM-py3.12/bin/python
cachedir: .pytest_cache
rootdir: /home/username/Documents/fastapi-demo
configfile: pyproject.toml
plugins: anyio-4.4.0
collected 20 items

tests/test_employee_data.py::EmployeeModelTest::test_employee_base_model_creation PASSED
tests/test_employee_data.py::EmployeeModelTest::test_employee_create_model_creation PASSED
tests/test_employee_data.py::EmployeeModelTest::test_employee_from_orm PASSED
tests/test_employee_data.py::EmployeeModelTest::test_employee_model_creation PASSED
tests/test_employee_data.py::EmployeeModelTest::test_employee_read_model_creation PASSED
tests/test_employee_data.py::EmployeeModelTest::test_employee_update_model_creation PASSED
tests/test_employee_model.py::EmployeeModelTest::test_employee_base_model_creation PASSED
tests/test_employee_model.py::EmployeeModelTest::test_employee_create_model_creation PASSED
tests/test_employee_model.py::EmployeeModelTest::test_employee_from_orm PASSED
tests/test_employee_model.py::EmployeeModelTest::test_employee_model_creation PASSED
tests/test_employee_model.py::EmployeeModelTest::test_employee_read_model_creation PASSED
tests/test_employee_model.py::EmployeeModelTest::test_employee_update_model_creation PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_create_employee PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_delete_employee PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_delete_employee_not_found PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_get_employee PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_get_employee_not_found PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_get_employees PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_update_employee PASSED
tests/test_employee_routes.py::EmployeeRouteTest::test_update_employee_not_found PASSED

============================================================ 20 passed in 1.72s ============================================================
```
5. If all the dependency is installed run the application by firing the command
```bash
$ poetry run run_app
```
