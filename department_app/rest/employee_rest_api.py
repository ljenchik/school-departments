"""
Employee REST API contains classes:
EmployeeSchema, SearchSchema, Employee, DepartmentEmployee, SearchEmployee
"""
# pylint: disable=cyclic-import
# pylint: disable=no-self-use
import http

from flask_apispec import marshal_with, use_kwargs, MethodResource, doc
from flask_restful import Resource, abort
from marshmallow import Schema, fields

from department_app.service.employee_service import create_employee_or_error, \
    get_employees_by_department_id, \
    delete_employee_by_id, get_employee_by_id, update_employee_or_error, \
    get_employee_by_dob, get_employee_by_period


class EmployeeSchema(Schema):
    """
    Swagger specs for employee
    """
    id = fields.Integer(required=False)
    name = fields.String(required=True, allow_none=False)
    role = fields.String(required=True, allow_none=False)
    date_of_birth = fields.DateTime(required=True, allow_none=False, format='%Y-%m-%d')
    salary = fields.Float(required=True, allow_none=False)
    department_id = fields.Integer(required=True, allow_none=False)
    start_date = fields.DateTime(required=True, allow_none=False, format='%Y-%m-%d')
    department_name = fields.String(required=False)


class SearchSchema(Schema):
    """
    Swagger specs for employee search request
    """
    date_of_birth = fields.DateTime(required=False, allow_none=False, format='%Y-%m-%d')
    date_from = fields.DateTime(required=False, allow_none=False, format='%Y-%m-%d')
    date_to = fields.DateTime(required=False, allow_none=False, format='%Y-%m-%d')


class Employee(MethodResource, Resource):
    """
    Employee REST API class
    """

    # decorator for swagger description
    @doc(description='Gets employee by id')
    @marshal_with(EmployeeSchema)
    def get(self, employee_id):
        """
        GET request to fetch employee by given id
        :return: employee
        """
        emp: dict = get_employee_by_id(employee_id)
        if emp is None:
            abort(http.HTTPStatus.NOT_FOUND)
        return emp

    @doc(description='Deletes employee by id')
    def delete(self, employee_id):
        """
        DELETE request
        Uses service to delete the employee by given id
        :return: empty dictionary, or a tuple with an error message and a status code 400
        in case of employee is not found
        """
        error: str = delete_employee_by_id(employee_id)
        if error is not None:
            return abort(http.HTTPStatus.BAD_REQUEST, error=error)
        return {}

    @doc(description='Updates employee')
    # Injects keyword arguments from the request as json
    @use_kwargs(EmployeeSchema, location=('json'))
    @marshal_with(EmployeeSchema)
    def put(self, employee_id, **kwargs):
        """
        PUT request to update employee's data
        :return: a tuple of updated employee in JSON format, or a
        tuple with error message and status code 400 in case of validation error
        """
        employee: dict = kwargs
        error, employee = update_employee_or_error(employee_id, employee)
        if error is not None:
            abort(http.HTTPStatus.BAD_REQUEST, error=error)
        return employee


class DepartmentEmployee(MethodResource, Resource):
    """
    DepartmentEmployee REST API class
    """

    @doc(description='Gets employees by department id')
    # serialization of the returned object to json()
    @marshal_with(EmployeeSchema(many=True))
    def get(self, department_id):
        """
        GET request to fetch employees of the department with given id
        :return: list of employees working in the department with given department_id
        """
        return get_employees_by_department_id(department_id)

    @doc(description='Creates a new employee')
    # Injects keyword arguments from the request as json
    @use_kwargs(EmployeeSchema, location='json')
    @marshal_with(EmployeeSchema)
    def post(self, department_id, **kwargs):
        """
        POST request to add new employee
        returns newly added employee in JSON format
        """
        employee: dict = kwargs  # returns employee dict from HTTP request
        employee['department_id'] = department_id
        (error, employee) = create_employee_or_error(employee)
        if error is not None:
            abort(http.HTTPStatus.BAD_REQUEST, error=error)
        return employee


class SearchEmployee(MethodResource, Resource):
    """
    SearchEmployee API class'
    """

    @doc(description='Searches employee date of birth')
    # 'query' because parameters are from url query
    @use_kwargs(SearchSchema, location='query')
    @marshal_with(EmployeeSchema(many=True))
    def get(self, **kwargs):
        """
        GET request to fetch employees with given date of birth or over a period
        between two given dates
        :return: list of employees with respective departments' names
        """
        search_args: dict = kwargs
        if 'date_of_birth' in search_args:
            return get_employee_by_dob(search_args['date_of_birth'])
        if 'date_from' in search_args and 'date_to' in search_args:
            return get_employee_by_period(search_args['date_from'], search_args['date_to'])
        abort(
            http.HTTPStatus.BAD_REQUEST,
            error='date_of_birth or date_from and date_to are required')
        return None
