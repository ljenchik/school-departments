# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring

import http
from unittest import TestCase
from unittest.mock import patch

from department_app import app
from department_app.tests.test_data import department_with_salaries_1


class MockResponse:  # pylint: disable=too-few-public-methods
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestDepartmentView(TestCase):

    def setUp(self) -> None:
        self.client = app.test_client()

    def test_departments(self):
        with patch(
                'department_app.views.department_view.requests'
        ) as requests_mock:
            response = self.client.get('/')
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            requests_mock.get.assert_called_once_with('http://localhost/api/departments')

    def test_edit_department_success(self):
        with patch(
                'department_app.views.department_view.requests.get',
                return_value=MockResponse(department_with_salaries_1, http.HTTPStatus.OK)
        ) as requests_mock:
            response = self.client.get('/department/edit/1')
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            requests_mock.assert_called_once_with('http://localhost/api/departments/1')

    def test_edit_department_not_found(self):
        with patch(
                'department_app.views.department_view.requests.get',
                return_value=MockResponse(None, http.HTTPStatus.NOT_FOUND)
        ) as requests_mock:
            response = self.client.get('/department/edit/123')
            self.assertEqual(http.HTTPStatus.NOT_FOUND, response.status_code)
            requests_mock.assert_called_once_with('http://localhost/api/departments/123')

    def test_edit_department_found(self):
        with patch(
                'department_app.views.department_view.requests.put',
                return_value=MockResponse({}, http.HTTPStatus.OK)
        ) as requests_mock:
            response = self.client.post(
                '/department/edit/123', data={'department_name': 'asdf asdfas'})
            self.assertEqual(http.HTTPStatus.FOUND, response.status_code)
            requests_mock.assert_called_once_with(
                'http://localhost/api/departments/123', data={'name': 'asdf asdfas'})

    def test_edit_department_with_error(self):
        # Setup
        with patch(
                'department_app.views.department_view.requests.put',
                return_value=MockResponse(
                    {'department_name': 'asdf asdfas', 'error': 'error_text'}, http.HTTPStatus.OK)
        ) as requests_mock:
            # Action
            response = self.client.post('/department/edit/123',
                                        data={'department_name': 'asdf asdfas', 'error': 'error_text'})
            # Asserts
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertIn('error_text', str(response.data))
            requests_mock.assert_called_once_with(
                'http://localhost/api/departments/123', data={'name': 'asdf asdfas'})

    def test_add_department_success(self):
        response = self.client.get('/department/add')
        self.assertEqual(http.HTTPStatus.OK, response.status_code)

    def test_add_department_with_error(self):
        # Setup
        with patch(
                'department_app.views.department_view.requests.post',
                return_value=MockResponse(
                    {'name': 'asdf asdfas', 'error': 'error_text'}, http.HTTPStatus.OK)
        ) as requests_mock:
            # Action
            response = self.client.post('/department/add',
                                        data={'department_name': 'asdf asdfas', 'id': None})
            # Asserts
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            self.assertIn('error_text', str(response.data))
            requests_mock.assert_called_once_with(
                'http://localhost/api/departments', data={'name': 'asdf asdfas'})

    def test_add_department_redirect(self):
        # Setup
        with patch(
                'department_app.views.department_view.requests.post',
                return_value=MockResponse(
                    {'name': 'asdf asdfas', 'id': 5, 'error': None}, http.HTTPStatus.OK)
        ) as requests_mock:
            # Action
            response = self.client.post('/department/add', data={'department_name': 'asdf asdfas'})
            # Asserts
            self.assertEqual(http.HTTPStatus.FOUND, response.status_code)
            requests_mock.assert_called_once_with(
                'http://localhost/api/departments', data={'name': 'asdf asdfas'})

    def test_delete_department(self):
        # Setup
        with patch(
                'department_app.views.department_view.requests.delete',
                return_value=MockResponse({}, http.HTTPStatus.OK)
        ) as requests_mock, patch(
            'department_app.views.department_view.requests.get',
            return_value=MockResponse([department_with_salaries_1], http.HTTPStatus.OK)
        ) as rest_api_get_mock:
            # Action
            response = self.client.post('/', data={'id': 5})
            # Asserts
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            requests_mock.assert_called_once_with('http://localhost/api/departments/5')
            rest_api_get_mock.assert_called_once_with('http://localhost/api/departments')

    def test_delete_department_error(self):
        # Setup
        with patch(
                'department_app.views.department_view.requests.delete',
                return_value=MockResponse({'error': 'error_text'}, http.HTTPStatus.OK)
        ) as requests_mock, patch(
            'department_app.views.department_view.requests.get',
            return_value=MockResponse([department_with_salaries_1], http.HTTPStatus.OK)
        ) as rest_api_get_mock:
            # Action
            response = self.client.post('/', data={'id': 5})
            # Asserts
            self.assertEqual(http.HTTPStatus.OK, response.status_code)
            requests_mock.assert_called_once_with('http://localhost/api/departments/5')
            self.assertIn('error_text', str(response.data))
            rest_api_get_mock.assert_called_once_with('http://localhost/api/departments')
