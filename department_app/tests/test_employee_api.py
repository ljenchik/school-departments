# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring
from datetime import datetime
import http
from unittest import TestCase
from unittest.mock import patch

from department_app import app
from department_app.models.employee import Employee
from department_app.tests.test_data import employee_1


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
