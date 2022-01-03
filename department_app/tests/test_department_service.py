# pylint: disable=missing-function-docstring, missing-module-docstring
"""
Unit tests for Department_service
"""
from unittest import TestCase
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from department_app.models.department_avg_salary import DepartmentAvgSalary
from department_app.models.department import Department
from department_app.service.department_service \
    import read_departments_with_salaries, get_department_by_id, \
    create_department_or_error, update_department, delete_department_by_id


class TestDepartmentService(TestCase):
    """
    Tests
    """

    @classmethod
    def test_read_departments_with_salaries(cls):
        with patch(
                'department_app.service.department_service.db.session'
        ) as db_session_mock:
            read_departments_with_salaries()
            db_session_mock.query(DepartmentAvgSalary).from_statement.assert_called_once()

    @classmethod
    def test_get_department_by_id(cls):
        with patch(
                'department_app.service.department_service.db.session'
        ) as db_session_mock:
            get_department_by_id(13)
            db_session_mock.query(Department).get.assert_called_once_with(13)

    def test_create_department_or_error(self):
        with patch(
                'department_app.service.department_service.db.session'
        ) as db_session_mock:
            error, return_value = create_department_or_error('Department_test')
            db_session_mock.add.assert_called_once_with(return_value)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(None, error)

    def test_create_department_or_error_fail_duplicate(self):
        with patch(
                'department_app.service.department_service.db.session',
        ) as db_session_mock:
            db_session_mock.add.side_effect = SQLAlchemyError('Duplicate')
            error, return_value = create_department_or_error('Department_test')

            db_session_mock.add.assert_called_once()
            db_session_mock.commit.assert_not_called()
            db_session_mock.rollback.assert_called_once()

            self.assertEqual('Department with this name already exists', error)
            self.assertEqual(None, return_value)

    def test_create_department_or_error_fail_unknown(self):
        with patch(
                'department_app.service.department_service.db.session',
        ) as db_session_mock:
            db_session_mock.add.side_effect = SQLAlchemyError('server error')
            error, return_value = create_department_or_error('Department_test')

            db_session_mock.add.assert_called_once()
            db_session_mock.commit.assert_not_called()
            db_session_mock.rollback.assert_called_once()

            self.assertEqual('server error', error)
            self.assertEqual(None, return_value)

    def test_update_department(self):
        with patch(
                'department_app.service.department_service.db.session'
        ) as db_session_mock:
            error, return_value = update_department(12, 'Department_test')  # pylint: disable=unused-variable
            db_session_mock.commit.assert_called_once()
            self.assertEqual(None, error)

    def test_update_department_fail_duplicate(self):
        with patch(
                'department_app.service.department_service.db.session',
        ) as db_session_mock:
            db_session_mock.commit.side_effect = SQLAlchemyError('Duplicate')
            error, return_value = update_department(12, 'Department_test')

            db_session_mock.commit.assert_called()
            db_session_mock.rollback.assert_called_once()

            self.assertEqual('Department with this name already exists', error)
            self.assertEqual(None, return_value)

    def test_update_department_or_error_fail_unknown(self):
        with patch(
                'department_app.service.department_service.db.session',
        ) as db_session_mock:
            db_session_mock.commit.side_effect = SQLAlchemyError('server error')
            error, return_value = update_department(12, 'Department_test')

            db_session_mock.commit.assert_called()
            db_session_mock.rollback.assert_called_once()

            self.assertEqual('server error', error)
            self.assertEqual(None, return_value)

    def test_delete_department_by_id(self):
        with patch(
                'department_app.service.department_service.db.session'
        ) as db_session_mock:
            return_value = delete_department_by_id(10)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(None, return_value)

    def test_delete_department_by_id_fail(self):
        with patch(
                'department_app.service.department_service.db.session',
        ) as db_session_mock:
            db_session_mock.delete.side_effect = SQLAlchemyError()
            returned_value = delete_department_by_id(12)
            db_session_mock.rollback.assert_called_once()
            self.assertEqual('You cannot delete department with employees', returned_value)
