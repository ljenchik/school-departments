"""
departments_rest_api.py defines two classes: DepartmentWithSalary and Department
"""
# pylint: disable=no-self-use
import http

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource, abort
from marshmallow import Schema, fields

from department_app.service.department_service import read_departments_with_salaries, \
    create_department_or_error, get_department_by_id, update_department, delete_department_by_id


class DepartmentWithSalarySchema(Schema):
    """
    Swagger specs of department with salaries class
    """
    id = fields.Integer()
    name = fields.String()
    avg_salary = fields.Float()


class DepartmentSchema(Schema):
    """
    Swagger specs of department class
    """
    id = fields.Integer()
    name = fields.String()
    error = fields.String(required=False)


class DepartmentNameSchema(Schema):
    """
    Swagger specs of incoming parameter for department name
    """
    name = fields.String(required=True, allow_none=False, error_messages={'required': 'error'})


class DepartmentWithSalary(MethodResource, Resource):
    """
    Department REST API Resource class
    """

    # decorator for swagger description
    @doc(description='Gets list of all departments with average employee salary')
    @marshal_with(DepartmentWithSalarySchema(many=True))  # decorator to serialize returned object
    def get(self):
        """
        GET request to fetch all departments with average salaries
        :return: list of all departments with average salaries in JSON format
        """
        return read_departments_with_salaries()

    @doc(description='Creates new department')
    # Injects keyword arguments from the request as json
    @use_kwargs(DepartmentNameSchema, location=('json'))
    @marshal_with(DepartmentSchema)
    def post(self, **kwargs):
        """
        POST request
        Deserializes request data, uses service to add department to
        database and returns newly added department in JSON format
        """
        error, new_department = create_department_or_error(kwargs['name'])
        if error is not None:
            abort(http.HTTPStatus.BAD_REQUEST, error=error)
        return new_department


class Department(MethodResource, Resource):
    """
    Department REST API Resource class
    """

    @doc(description='Gets department by id')
    @marshal_with(DepartmentSchema)
    def get(self, department_id):
        """
        GET request to fetch all departments via service
        :return: list of all departments in JSON format
        """
        dep = get_department_by_id(department_id)
        if dep is None:
            abort(http.HTTPStatus.NOT_FOUND)
        return dep

    @doc(description='Updates department by id')
    @use_kwargs(DepartmentNameSchema, location=('json'))
    @marshal_with(DepartmentSchema)
    def put(self, department_id: int, name: str):
        """
        PUT request to deserialize request data, finds the department with
        given department_id and updates it
        :return: a tuple of updated department in JSON format and status code 202, or a
        tuple of error messages and status code 400 in case of validation error
        """
        error, department = update_department(department_id, name)
        if error is not None:  # if there is an error the function returns dictionary with error
            abort(http.HTTPStatus.BAD_REQUEST, error=error)
        return department, http.HTTPStatus.OK

    @doc(description='Deletes department by id')
    def delete(self, department_id):
        """
        DELETE request to delete the department with given department id
        :return: empty dictionary or a tuple of an error message and a status code 400
        """
        error = delete_department_by_id(department_id)
        if error is not None:
            abort(http.HTTPStatus.BAD_REQUEST, error=error)
        return {}
