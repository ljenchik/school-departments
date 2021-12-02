from datetime import datetime

from service.department_service import read_departments_with_salaries, create_department_or_error, get_department_by_id, \
    update_department, delete_department_by_id
from flask_restful import Resource, fields, marshal_with, reqparse

from service.employee_service import create_employee_or_error

department_put_args:reqparse.RequestParser = reqparse.RequestParser()
department_put_args.add_argument('name', type = str, required=True, help='Name of department')

employee_parse_args:reqparse.RequestParser = reqparse.RequestParser()
employee_parse_args.add_argument('name', type = str, required=True, help='Name of employee')
employee_parse_args.add_argument('role', type = str, required=True, help='Role of employee')
employee_parse_args.add_argument('date_of_birth', type = datetime,  required=True, help='Date of birth of employee')
employee_parse_args.add_argument('salary', type = float, required=True, help='Salary of employee')
employee_parse_args.add_argument('department_id', type = int, required=True, help='Id of department')
employee_parse_args.add_argument('start_date', type = datetime, required=True, help='Start date')

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

employee_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'role' : fields.String,
    'date_of_birth' : fields.DateTime,
    'salary' : fields.Float,
    'start_date' : fields.DateTime,
    'department_id' : fields.Integer,
    'error' : fields.String,
}


class DepartmentWithSalary(Resource):
    @marshal_with(department_with_salary_fields)
    def get(self):
        return read_departments_with_salaries()

    @marshal_with(department_fields)
    def post(self):
        args = department_put_args.parse_args()      # serialization of the returned object from this method (returns department with 3 fields in the form of dictionary)
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

    @marshal_with(department_fields)            # serialization of the returned object from this method (returns department with 3 fields in the form of dictionary)
    def put(self, department_id: int):
        args:dict = department_put_args.parse_args()                 # get the name of the department from the request body
        error, department = update_department(department_id, args['name'])     # tries to save to db and returns error (empty name or duplicate) if unsuccesful
        if error is not None:                                   # if there is an error the function returns dictionary with error
            return {'error' : error}, 500                       # 500 is http response code which means server failed
        return department, 202                                  # if there is no error the function returns updated department


    def delete(self, department_id):
        error = delete_department_by_id(department_id)
        if error is not None:
            return {'error' : error}, 500
        else:
            return {}



class Employee(Resource):
    @marshal_with(employee_fields)      # serialization of the returned object to json)
    def post(self): #add employee
        args:dict = employee_parse_args.parse_args()
        (error, employee) = create_employee_or_error(args)
        if error is not None:
            return {'error': error}, 500
        return employee