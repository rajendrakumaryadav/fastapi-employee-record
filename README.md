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

6. Open the browser and navigate to `https://localhost:5000/docs`
> It will open swagger docs page. Where you can interact the with API server. Here is Terminal Output.
```bash
$ poetry run run_app
INFO:     Will watch for changes in these directories: ['/home/username/Documents/fastapi-demo']
INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [151986] using StatReload
INFO:     Started server process [151994]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
## Frontend
---
7, Frontend is added to the service, once service is running we can open any browser of choice open the page.
8. Default, It would be available at `http://localhost:5000/`
Default page:
![Screenshot from 2024-09-01 02-01-08](https://github.com/user-attachments/assets/833c4b9b-981f-4bb2-a0d0-16b71e97f373)
