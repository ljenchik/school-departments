from service.department_service import read_departments_with_salaries, create_department_or_error, get_department_by_id, \
    update_department, delete_department_by_id

from flask_restful import Api, Resource, fields, marshal_with, reqparse

from flask import Blueprint

account_api = Blueprint('account_api', __name__)

department_put_args = reqparse.RequestParser()
department_put_args.add_argument('name', type = str, required=True, help='Name of department')

department_with_salary_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'salary' : fields.Float,
}

department_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'error' : fields.String
}

class DepartmentWithSalary(Resource):
    @marshal_with(department_with_salary_fields)
    def get(self):
        return read_departments_with_salaries()

    @marshal_with(department_fields)
    def post(self):
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

    @marshal_with(department_fields)
    def put(self, department_id: int):
        args = department_put_args.parse_args()
        error = update_department(department_id, args.name)
        if error is not None:
            return {'error' : error}, 500

        return get_department_by_id(department_id), 201



    def delete(self, department_id):
        error = delete_department_by_id(department_id)
        if error is not None:
            return {'error' : error}, 500
        else:
            return {}



