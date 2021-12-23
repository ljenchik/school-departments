"""
Departments_rest_api.py, this module defines the following classes:
- `DepartmentWithSalary`, department API class
- `Department`, department API class
"""

from flask_restful import Resource, fields, marshal_with, reqparse

from department_app.service.department_service import read_departments_with_salaries, \
    create_department_or_error, get_department_by_id, update_department, delete_department_by_id

department_request_parser: reqparse.RequestParser = reqparse.RequestParser()
department_request_parser.add_argument('name', type=str, required=True, help='Name of department')

department_with_salary_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'avg_salary': fields.Float,
}

department_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'error': fields.String
}


class DepartmentWithSalary(Resource):
    """
    Department API class
    """

    @marshal_with(department_with_salary_fields)
    def get(self):
        """
        GET request handler of department with salary api
        Fetches all departments with average salaries via service and returns them in a JSON format
        :return: all departments with average salaries JSON
        """
        return read_departments_with_salaries()

    @marshal_with(department_fields)  # serialization of the returned object from this method
    def post(self):
        """
        POST request handler of department with salary API
        Deserializes request data, uses service to add the department to the
        database and returns newly added department in a JSON format
        """
        args: dict = department_request_parser.parse_args()
        if args['name'] == '':
            return {'error': 'Department name must be set'}, 500

        error, new_department = create_department_or_error(args['name'])
        if error is not None:
            return {'error': error, 'name': args['name']}, 500
        return new_department


class Department(Resource):
    """
    Department API class
    """

    @marshal_with(department_fields)
    def get(self, department_id):
        """
        GET request handler of department
        Fetches all departments via service and returns them in a JSON format
        :return: all departments in JSON
        """
        return get_department_by_id(department_id)

    # serialization of the returned object from this method
    # (returns department with 3 fields in the form of dictionary)
    @marshal_with(department_fields)
    def put(self, department_id: int):
        """
        PUT request handler of department API
        Uses service to deserialize request data and find the department with
        given department_id and update it with deserialized instance, returns updated
        department in a JSON format with a status code 202 (Accepted)
        or returns error messages with a status code 500 (Bad Request) in case of
        validation error during deserialization
        :return: a tuple of updated department JSON and status code 202, or a
        tuple of error messages and status code 500 in case of validation
        error
        """
        args: dict = department_request_parser.parse_args()  # get the name of the department
        # from the request body
        error, department = update_department(department_id, args['name'])
        # tries to save to db and returns error (empty name or duplicate) if unsuccessful
        if error is not None:  # if there is an error the function returns dictionary with error
            return {'error': error}, 500  # 500 is http response code which means server failed
        return department, 202  # if there is no error the function returns updated department

    def delete(self, department_id):
        """
        DELETE request handler of department API
        Uses service to delete the department with given department
        :return: empty dictionary or a tuple of an error message and a status code 500
        in case of department with given department id not being found
        """
        error = delete_department_by_id(department_id)
        if error is not None:
            return {'error': error}, 500
        return {}
