# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring

import http
from unittest import TestCase
from unittest.mock import patch

from department_app import app
from department_app.tests.test_data import employee_1


class MockResponse:  # pylint: disable=too-few-public-methods
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestEmployeetView(TestCase):

    def setUp(self) -> None:
        self.client = app.test_client()

    def test_index_employee(self):
        with patch(
                'department_app.views.employee_view.get_department_by_id',
                return_value={}
        ) as requests_mock, patch(  # pylint: disable=unused-variable
            'department_app.views.employee_view.requests.get',
            return_value=MockResponse([employee_1], http.HTTPStatus.OK)
        ) as requests_employees:
            response = self.client.get('/department/1/employees')
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            requests_employees.assert_called_once_with(
                'http://localhost//api/department/1/employee')
