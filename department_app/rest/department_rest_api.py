"""
departments_rest_api.py defines two classes: DepartmentWithSalary and Department
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
    Department REST API class
    """

    @marshal_with(department_with_salary_fields)
    def get(self):
        """
        GET request to fetch all departments with average salaries
        :return: all departments with average salaries in JSON format
        """
        return read_departments_with_salaries()

    @marshal_with(department_fields)  # serialization of the returned object
    def post(self):
        """
        POST request
        Deserializes request data, uses service to add department to
        database and returns newly added department in JSON format
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
    Department REST API class
    """

    @marshal_with(department_fields)
    def get(self, department_id):
        """
        GET request to fetch all departments via service
        :return: all departments in JSON format
        """
        return get_department_by_id(department_id)

    # serialization of the returned object from this method
    # (returns department with 3 fields in the form of dictionary)
    @marshal_with(department_fields)
    def put(self, department_id: int):
        """
        PUT request to deserialize request data, find the department with
        given department_id and update it
        :return: a tuple of updated department in JSON format and status code 202, or a
        tuple of error messages and status code 500 in case of validation error
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
        DELETE request to delete the department with given department id
        :return: empty dictionary or a tuple of an error message and a status code 500
        """
        error = delete_department_by_id(department_id)
        if error is not None:
            return {'error': error}, 500
        return {}
