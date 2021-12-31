# pylint: disable=missing-function-docstring, missing-module-docstring
"""
Unit tests for Department_service
"""
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from department_app.models.employee import Employee
from department_app.service.employee_service \
    import get_employees_by_department_id, create_employee_or_error, \
    update_employee_or_error, delete_employee_by_id, \
    get_employee_by_id, get_employee_by_dob, get_employee_by_period, \
    validate_employee


class TestEmployeetService(TestCase):
    """
    Tests
    """

    @classmethod
    def test_get_employees_by_department_id(cls):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            get_employees_by_department_id(12)
            db_session_mock.query(Employee).filter_by.assert_called_once_with(department_id=12)

    def test_create_employee_or_error(self):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            args = {'name': 'Bob Marley', 'role': 'Teacher',
                    'date_of_birth': datetime(1982, 12, 4),
                    'salary': 37453.0, 'start_date': datetime(2012, 9, 3)}
            error, return_value = create_employee_or_error(args)
            db_session_mock.add.assert_called_once_with(return_value)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(None, error)

    def test_create_employee_or_error_fail(self):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            db_session_mock.add.side_effect = SQLAlchemyError()
            args = {'name': 'Bob Marley', 'role': 'Teacher',
                    'date_of_birth': datetime(1982, 12, 4),
                    'salary': 37453.0, 'start_date': datetime(2012, 9, 3)}
            error, return_value = create_employee_or_error(args)

            db_session_mock.add.assert_called_once()
            db_session_mock.commit.assert_not_called()
            db_session_mock.rollback.assert_called_once()

            self.assertEqual('There was an issue adding a new employee ()', error)
            self.assertEqual(None, return_value)

    def test_update_employee_or_error(self):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            args = {'name': 'Bob Marley', 'role': 'Teacher',
                    'date_of_birth': datetime(1982, 12, 4),
                    'salary': 37453.0, 'start_date': datetime(2012, 9, 3)}
            error, return_value = update_employee_or_error(4, args)  # pylint: disable=unused-variable
            db_session_mock.commit.assert_called()
            self.assertEqual(None, error)

    def test_update_employee_or_error_fail(self):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            db_session_mock.commit.side_effect = SQLAlchemyError()
            args = {'name': 'Bob Marley', 'role': 'Teacher',
                    'date_of_birth': datetime(1982, 12, 4),
                    'salary': 37453.0, 'start_date': datetime(2012, 9, 3)}
            error, return_value = update_employee_or_error(4, args)

            db_session_mock.commit.assert_called()
            db_session_mock.rollback.assert_called_once()

            self.assertEqual('There was an issue editing an employee: ()', error)
            self.assertEqual(None, return_value)

    def test_delete_employee_by_id(self):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            return_value = delete_employee_by_id(10)
            db_session_mock.commit.assert_called_once()
            self.assertEqual(None, return_value)

    def test_delete_employee_by_id_fail(self):
        with patch(
                'department_app.service.employee_service.db.session',
        ) as db_session_mock:
            db_session_mock.delete.side_effect = SQLAlchemyError()
            returned_value = delete_employee_by_id(12)
            db_session_mock.rollback.assert_called_once()
            self.assertEqual('There was an issue deleting this employee', returned_value)

    @classmethod
    def test_get_employee_by_id(cls):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            get_employee_by_id(13)
            db_session_mock.query(Employee).get.assert_called_once_with(13)

    @classmethod
    def test_get_employee_by_dob(cls):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            get_employee_by_dob('1985-09-08')
            db_session_mock.query(Employee).from_statement.assert_called_once()

    @classmethod
    def test_get_employee_by_period(cls):
        with patch(
                'department_app.service.employee_service.db.session'
        ) as db_session_mock:
            get_employee_by_period('1985-09-08', '1990-01-01')
            db_session_mock.query(Employee).from_statement.assert_called_once()

    def test_validate_employee_success(self):
        args = {'name': 'Bob Marley', 'role': 'Teacher',
                'date_of_birth': datetime(1982, 12, 4),
                'salary': 37453.0, 'start_date': datetime(2012, 9, 3)}
        self.assertEqual(None, validate_employee(args))

    def test_validate_employee_fail1(self):
        args = {'name': 'Bob Marley', 'role': 'Teacher',
                'date_of_birth': datetime(1982, 12, 4),
                'salary': 37453.0, 'start_date': datetime(1991, 9, 3)}
        self.assertEqual('Employee must be at least 18 to start work', validate_employee(args))

    def test_validate_employee_fail2(self):
        args = {'name': 'Bob Marley', 'role': 'Teacher',
                'date_of_birth': datetime(1900, 12, 4),
                'salary': 37453.0, 'start_date': datetime(1991, 9, 3)}
        self.assertEqual("Please check employee's date of birth", validate_employee(args))

    def test_validate_employee_fail3(self):
        args = {'name': 'Bob Marley', 'role': 'Teacher',
                'date_of_birth': datetime(2012, 12, 4),
                'salary': 37453.0, 'start_date': datetime(1991, 9, 3)}
        self.assertEqual("Please check employee's date of birth", validate_employee(args))
       