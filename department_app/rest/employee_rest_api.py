"""
Employee REST API contains classes: IsoDateFormat, Employee, DepartmentEmployee, SearchEmployee
"""
# pylint: disable=cyclic-import
from datetime import datetime

from flask_restful import Resource, fields, marshal_with, reqparse

from department_app.service.employee_service import create_employee_or_error, \
    get_employees_by_department_id, \
    delete_employee_by_id, get_employee_by_id, update_employee_or_error, \
    get_employee_by_dob, get_employee_by_period

employee_parse_args: reqparse.RequestParser = reqparse.RequestParser()
employee_parse_args.add_argument('name', type=str, required=True, help="Employee's name")
employee_parse_args.add_argument('role', type=str, required=True, help="Employee's role")
employee_parse_args.add_argument('date_of_birth', type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                                 required=True, help='Date of birth of employee')
employee_parse_args.add_argument('salary', type=float, required=True, help="Employee's salary")
employee_parse_args.add_argument('department_id', type=int, required=True, help='Department id')
employee_parse_args.add_argument('start_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                                 required=True, help='Start date')

searchemployee_parse_args: reqparse.RequestParser = reqparse.RequestParser()
searchemployee_parse_args.add_argument('date_of_birth',
                                       type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
searchemployee_parse_args.add_argument('date_from', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
searchemployee_parse_args.add_argument('date_to', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))


class IsoDateFormat(fields.Raw):
    """
    Employee REST API class
    """

    def format(self, value):
        return value.strftime('%Y-%m-%d')


employee_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'role': fields.String,
    'date_of_birth': IsoDateFormat,
    'salary': fields.Float,
    'start_date': IsoDateFormat,
    'department_id': fields.Integer,
    'error': fields.String,
}


class Employee(Resource):
    """
    Employee REST API class
    """

    @classmethod
    @marshal_with(employee_fields)
    def get(cls, employee_id):
        """
        GET request to fetch employee by her/his id
        :return: employee
        """
        employee_to_edit: dict = get_employee_by_id(employee_id)
        return employee_to_edit

    @classmethod
    def delete(cls, employee_id):
        """
        DELETE request
        Uses service to delete the employee by employee id
        :return: empty dictionary or a tuple of an error message and a status code 500
        in case of employee is not found
        """
        error: str = delete_employee_by_id(employee_id)
        if error is not None:
            return {'error': error}, 500
        return {}

    @classmethod
    @marshal_with(employee_fields)
    def put(cls, employee_id):
        """
        PUT request to update employee's data
        :return: a tuple of updated employee in JSON format, or a
        tuple of error message and status code 500 in case of validation error
        """
        args: dict = employee_parse_args.parse_args()  # returns employee dict from flask request
        error, employee = update_employee_or_error(employee_id, args)
        if error is not None:
            return {'error': error}, 500
        return employee


class DepartmentEmployee(Resource):
    """
    DepartmentEmployee REST API class
    """

    @classmethod
    @marshal_with(employee_fields)  # serialization of the returned object to json()
    def get(cls, department_id):
        """
        GET request handler of DepartmentEmployee API
        :return: employees working in the department with a given department_id
        """
        return get_employees_by_department_id(department_id)

    @classmethod
    @marshal_with(employee_fields)  # serialization of the returned object to json
    def post(cls, department_id):
        """
        POST request to add new employee
        returns newly added employee in JSON format
        """
        args: dict = employee_parse_args.parse_args()  # returns employee dict from flask request
        args['department_id'] = department_id
        (error, employee) = create_employee_or_error(args)
        if error is not None:
            return {'error': error}, 500
        return employee


employee_dep_name_fields = employee_fields.copy()
employee_dep_name_fields['department_name'] = fields.String


class SearchEmployee(Resource):
    """
    SearchEmployee API class
    """

    @classmethod
    @marshal_with(employee_dep_name_fields)  # serialization of the returned object to json()
    def get(cls):
        """
        GET request to fetch emloyees with given date of birth or over a period
        between two given dates
        :return: employees with respective department names
        """
        args: dict = searchemployee_parse_args.parse_args()
        if args['date_of_birth'] is not None:
            return get_employee_by_dob(args['date_of_birth'])
        if args['date_from'] is not None and args['date_to'] is not None:
            return get_employee_by_period(args['date_from'], args['date_to'])
        return None
