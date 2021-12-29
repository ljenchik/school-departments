# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring
import http
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from department_app import app
from department_app.models.employee import Employee
from department_app.tests.test_data import employee_1, employee_2, employee_4


def employee_to_json(employee: Employee) -> dict:
    employee_dict: dict = {c.name: getattr(employee, c.name)
                           for c in employee.__table__.columns if
                           c.name != "date_created"
                           }
    employee_dict['error'] = None
    employee_dict['start_date'] = datetime.strftime(employee.start_date, '%Y-%m-%d')
    employee_dict['date_of_birth'] = datetime.strftime(employee.date_of_birth, '%Y-%m-%d')
    return employee_dict


class TestEmployeetApi(TestCase):
    # pylint: disable=no-self-use

    def setUp(self) -> None:
        self.client = app.test_client()

    def test_get_employee(self):
        mock_return_value = employee_1
        with patch(
                'department_app.rest.employee_rest_api.get_employee_by_id',
                return_value=mock_return_value
        ) as get_employee_by_id_mock:
            response = self.client.get('/api/employee/1')
            expected_json = employee_to_json(employee_1)

            get_employee_by_id_mock.assert_called_once_with(1)
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(expected_json, response.json)

    def test_delete_employee_by_id_success(self):
        with patch(
                'department_app.rest.employee_rest_api.delete_employee_by_id',
                return_value=None
        ) as delete_employee_by_id:
            response = self.client.delete('/api/employee/1')

            delete_employee_by_id.assert_called_once_with(1)
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual({}, response.json)

    def test_delete_employee_by_id_fail(self):
        with patch(
                'department_app.rest.employee_rest_api.delete_employee_by_id',
                return_value='There was an issue deleting this employee'
        ) as delete_employee_by_id:
            response = self.client.delete('/api/employee/3')

            delete_employee_by_id.assert_called_once_with(3)
            self.assertEqual(http.HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)
            self.assertEqual(
                {'error': 'There was an issue deleting this employee'}, response.json)

    def test_update_employee_success(self):
        with patch(
                'department_app.rest.employee_rest_api.update_employee_or_error',
                return_value=(None, employee_2)
        ) as update_employee_or_error:
            updated_employee = {'name': 'req name', 'role': 'req role', 'date_of_birth': '1981-12-12',
                                'salary': 23456.0, 'start_date': '2018-09-03', 'department_id': 2}
            response = self.client.put('/api/employee/2', data=updated_employee)

            # rest api converts string dates into python datetime objects
            updated_employee['date_of_birth'] = datetime(1981, 12, 12, 0, 0)
            updated_employee['start_date'] = datetime(2018, 9, 3, 0, 0)
            update_employee_or_error.assert_called_once_with(2, updated_employee)

            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(employee_to_json(employee_2), response.json)

    def test_get_employees_by_department_id(self):
        mock_return_value = [employee_2, employee_4]
        with patch(
                'department_app.rest.employee_rest_api.get_employees_by_department_id',
                return_value=mock_return_value
        ) as get_employees_by_department_id:
            response = self.client.get('/api/department/2/employee')
            expected_json = [employee_to_json(d) for d in mock_return_value]

            get_employees_by_department_id.assert_called_once_with(2)
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(expected_json, response.json)

    def test_add_employee_success(self):
        with patch(
                'department_app.rest.employee_rest_api.create_employee_or_error',
                return_value=(None, employee_2)
        ) as create_employee_or_error:
            # rest api request
            added_employee = {'name': 'Alex Brown', 'role': 'Teacher', 'date_of_birth': '1992-2-15',
                              'salary': 27453.0, 'start_date': '2015-09-03', 'department_id': 2}
            response = self.client.post('/api/department/2/employee', data=added_employee)

            employee_sent_to_service = added_employee.copy()
            employee_sent_to_service['date_of_birth'] = datetime(1992, 2, 15)
            employee_sent_to_service['start_date'] = datetime(2015, 9, 3)
            create_employee_or_error.assert_called_once_with(employee_sent_to_service)

            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(employee_to_json(employee_2), response.json)

    def test_add_employee_fail(self):
        with patch(
                'department_app.rest.employee_rest_api.create_employee_or_error',
                return_value=('There was an issue adding a new employee ', None)
        ) as create_employee_or_error:
            # rest api request
            added_employee = {'name': 'Alex Brown', 'role': 'Teacher', 'date_of_birth': '1992-2-15',
                              'salary': 27453.0, 'start_date': '2015-09-03', 'department_id': 2}
            response = self.client.post('/api/department/2/employee', data=added_employee)

            added_employee['date_of_birth'] = datetime(1992, 2, 15)
            added_employee['start_date'] = datetime(2015, 9, 3)
            create_employee_or_error.assert_called_once_with(added_employee)

            self.assertEqual(http.HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)
            self.assertEqual({'date_of_birth': None,
                              'department_id': 0,
                              'error': 'There was an issue adding a new employee ',
                              'id': 0,
                              'name': None,
                              'role': None,
                              'salary': None,
                              'start_date': None}, response.json)
