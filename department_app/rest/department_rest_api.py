from flask_restful import Resource, fields, marshal_with, reqparse

from department_app.service.department_service import read_departments_with_salaries, create_department_or_error, \
    get_department_by_id, update_department, delete_department_by_id

department_put_args: reqparse.RequestParser = reqparse.RequestParser()
department_put_args.add_argument('name', type=str, required=True, help='Name of department')

department_with_salary_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'salary': fields.Float,
}

department_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'error': fields.String
}


class DepartmentWithSalary(Resource):
    @marshal_with(department_with_salary_fields)
    def get(self):
        return read_departments_with_salaries()

    @marshal_with(department_fields)
    def post(self):
        # serialization of the returned object from this method
        # returns department with 3 fields in the form of dictionary
        args = department_put_args.parse_args()
        if args['name'] == '':
            return {'error': 'Department name must be set'}, 500

        error, new_department = create_department_or_error(args['name'])
        if error is not None:
            return {'error': error, 'name': args['name']}, 500
        else:
            return new_department


class Department(Resource):
    @marshal_with(department_fields)
    def get(self, department_id):
        return get_department_by_id(department_id)

    # serialization of the returned object from this method (returns department with 3 fields in the form of dictionary)
    @marshal_with(department_fields)
    def put(self, department_id: int):
        args: dict = department_put_args.parse_args()  # get the name of the department from the request body
        error, department = update_department(department_id, args[
            'name'])  # tries to save to db and returns error (empty name or duplicate) if unsuccesful
        if error is not None:  # if there is an error the function returns dictionary with error
            return {'error': error}, 500  # 500 is http response code which means server failed
        return department, 202  # if there is no error the function returns updated department

    def delete(self, department_id):
        error = delete_department_by_id(department_id)
        if error is not None:
            return {'error': error}, 500
        else:
            return {}
