# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring
import http
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from department_app import app
from department_app.models.employee import Employee
from department_app.tests.test_data \
    import employee_1, employee_2, employee_4, employee_5, employee_3


def employee_to_json(employee: Employee) -> dict:
    employee_dict: dict = {c.name: getattr(employee, c.name)
                           for c in employee.__table__.columns if
                           c.name != "date_created"
                           }
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
            self.assertEqual(http.HTTPStatus.BAD_REQUEST, response.status_code)
            self.assertEqual(
                {'error': 'There was an issue deleting this employee'}, response.json)

    def test_update_employee_success(self):
        with patch(
                'department_app.rest.employee_rest_api.update_employee_or_error',
                return_value=(None, employee_2)
        ) as update_employee_or_error:
            updated_employee = {
                'name': 'req name', 'role': 'req role', 'date_of_birth': '1981-12-12',
                'salary': 23456.0, 'start_date': '2018-09-03', 'department_id': 2
            }
            response = self.client.put('/api/employee/2', json=updated_employee)

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
            response = self.client.post('/api/department/2/employee', json=added_employee)

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
            response = self.client.post('/api/department/2/employee', json=added_employee)

            added_employee['date_of_birth'] = datetime(1992, 2, 15)
            added_employee['start_date'] = datetime(2015, 9, 3)
            create_employee_or_error.assert_called_once_with(added_employee)

            self.assertEqual(http.HTTPStatus.BAD_REQUEST, response.status_code)
            self.assertEqual({'error': 'There was an issue adding a new employee '}, response.json)

    def test_search_employees_dob_success(self):
        mock_return_value = [employee_5]
        with patch(
                'department_app.rest.employee_rest_api.get_employee_by_dob',
                return_value=mock_return_value
        ) as get_employee_by_dob:
            response = self.client.get('/api/employee/search?date_of_birth=1975-01-01')

            expected_json = [employee_to_json(employee_5)]
            get_employee_by_dob.assert_called_once_with(datetime(1975, 1, 1))

            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(expected_json, response.json)

    def test_search_employees_dob_fail(self):
        mock_return_value = []
        with patch(
                'department_app.rest.employee_rest_api.get_employee_by_dob',
                return_value=mock_return_value
        ) as get_employee_by_dob:
            response = self.client.get('/api/employee/search')

            get_employee_by_dob.assert_not_called()

            self.assertEqual(http.HTTPStatus.BAD_REQUEST, response.status_code)
            self.assertEqual(
                {'error': 'date_of_birth or date_from and date_to are required'}, response.json)

    def test_search_employees_period_success(self):
        mock_return_value = [employee_3, employee_5]
        with patch(
                'department_app.rest.employee_rest_api.get_employee_by_period',
                return_value=mock_return_value
        ) as get_employee_by_period:
            response = self.client.get(
                '/api/employee/search?date_from=1974-12-12&date_to=1983-01-01')

            expected_json = [employee_to_json(d) for d in mock_return_value]
            get_employee_by_period.assert_called_once_with(
                datetime(1974, 12, 12), datetime(1983, 1, 1))

            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(expected_json, response.json)

    def test_search_employees_period_fail_invalid_date(self):
        mock_return_value = [employee_3, employee_5]
        with patch(
                'department_app.rest.employee_rest_api.get_employee_by_period',
                return_value=mock_return_value
        ) as get_employee_by_period:
            response = self.client.get \
                ('/api/employee/search?date_from=1974-23-12&date_to=1983-01-01')

            get_employee_by_period.assert_not_called()

            self.assertEqual(http.HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)
