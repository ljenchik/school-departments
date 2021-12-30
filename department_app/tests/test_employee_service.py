# pylint: disable=missing-function-docstring, missing-module-docstring
"""
Unit tests for Department_service
"""
from unittest import TestCase
from unittest.mock import patch

from department_app.models.employee import Employee
from department_app.service.employee_service import get_employees_by_department_id


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
