# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring

import http
from unittest import TestCase
from unittest.mock import patch

from department_app import app
from department_app.models.department_avg_salary import DepartmentAvgSalary
from department_app.tests.test_data \
    import department_with_salaries_1, department_with_salaries_2, department_1


def department_to_json(department: DepartmentAvgSalary) -> dict:
    department_dict: dict = {c.name: getattr(department, c.name)
                             for c in department.__table__.columns if
                             c.name != "date_created"
                             }
    return department_dict


class TestDepartmentApi(TestCase):
    # pylint: disable=no-self-use

    def setUp(self) -> None:
        self.client = app.test_client()

    def test_get_departments_with_avg_salary(self):
        mock_return_value = [department_with_salaries_1, department_with_salaries_2]
        with patch(
                'department_app.rest.department_rest_api.read_departments_with_salaries',
                return_value=mock_return_value
        ) as get_departments_mock:
            response = self.client.get('/api/departments')
            expected_json = [department_to_json(d) for d in mock_return_value]

            get_departments_mock.assert_called_once_with()
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(expected_json, response.json)

    def test_add_department_success(self):
        with patch(
                'department_app.rest.department_rest_api.create_department_or_error',
                return_value=(None, department_1)
        ) as create_department_or_error:
            response = self.client.post('/api/departments', json={'name': 'Requested name'})

            create_department_or_error.assert_called_once_with('Requested name')
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual(
                {'id': department_1.id, 'name': department_1.name},
                response.json)

    def test_add_department_fail_already_exists(self):
        with patch(
                'department_app.rest.department_rest_api.create_department_or_error',
                return_value=('Department with this name already exist', None)
        ) as create_department_or_error:
            response = self.client.post('/api/departments', json={'name': 'Requested name'})

            create_department_or_error.assert_called_once_with('Requested name')
            self.assertEqual(http.HTTPStatus.BAD_REQUEST, response.status_code)
            self.assertEqual(
                {'error': 'Department with this name already exist'},
                response.json)

    def test_add_department_fail_empty(self):
        response = self.client.post('/api/departments')
        self.assertEqual(http.HTTPStatus.UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_departments_by_id(self):
        mock_return_value = department_1
        with patch(
                'department_app.rest.department_rest_api.get_department_by_id',
                return_value=mock_return_value
        ) as get_department_by_id_mock:
            response = self.client.get('/api/departments/3')

            get_department_by_id_mock.assert_called_once_with(3)
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual({'id': 3, 'name': 'Dep of Maths Test'}, response.json)

    def test_update_department_success(self):
        with patch(
                'department_app.rest.department_rest_api.update_department',
                return_value=(None, department_1)
        ) as update_department:
            response = self.client.put('/api/departments/3', json={'name': 'Requested name'})

            update_department.assert_called_once_with(3, 'Requested name')
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual({'id': 3, 'name': 'Dep of Maths Test'}, response.json)

    def test_update_department_fail(self):
        with patch(
                'department_app.rest.department_rest_api.update_department',
                return_value=('Department with this name already exist', None)
        ) as update_department:
            response = self.client.put('/api/departments/3', json={'name': 'Requested name'})

            update_department.assert_called_once_with(3, 'Requested name')
            self.assertEqual(http.HTTPStatus.BAD_REQUEST, response.status_code)
            self.assertEqual(
                {'error': 'Department with this name already exist'},
                response.json
            )

    def test_delete_department_by_id_success(self):
        with patch(
                'department_app.rest.department_rest_api.delete_department_by_id',
                return_value=None
        ) as delete_department_by_id:
            response = self.client.delete('/api/departments/3')

            delete_department_by_id.assert_called_once_with(3)
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertEqual({}, response.json)

    def test_delete_department_by_id_fail(self):
        with patch(
                'department_app.rest.department_rest_api.delete_department_by_id',
                return_value='You cannot delete department with employees'
        ) as delete_department_by_id:
            response = self.client.delete('/api/departments/3')

            delete_department_by_id.assert_called_once_with(3)
            self.assertEqual(http.HTTPStatus.BAD_REQUEST, response.status_code)
            self.assertEqual(
                {'error': 'You cannot delete department with employees'}, response.json)
