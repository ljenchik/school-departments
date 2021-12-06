from datetime import datetime

from flask_restful import Resource, fields, marshal_with, reqparse

from department_app.service.employee_service import create_employee_or_error, get_employees_by_department_id, \
    delete_employee_by_id, get_employee_by_id, update_employee_or_error

department_put_args: reqparse.RequestParser = reqparse.RequestParser()
department_put_args.add_argument('name', type=str, required=True, help='Name of department')

employee_parse_args: reqparse.RequestParser = reqparse.RequestParser()
employee_parse_args.add_argument('name', type=str, required=True, help="Employee's name")
employee_parse_args.add_argument('role', type=str, required=True, help="Employee's role")
employee_parse_args.add_argument('date_of_birth', type=lambda x: datetime.strptime(x,'%Y-%m-%d'), required=True,
                                 help='Date of birth of employee')
employee_parse_args.add_argument('salary', type=float, required=True, help="Employee's salary")
employee_parse_args.add_argument('department_id', type=int, required=True, help='Department id')
employee_parse_args.add_argument('start_date', type=lambda x: datetime.strptime(x,'%Y-%m-%d'),
                                 required=True, help='Start date')


class IsoDateFormat(fields.Raw):
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
    @marshal_with(employee_fields)
    def get(self, employee_id):
        employee_to_edit: dict = get_employee_by_id(employee_id)
        return employee_to_edit


    @marshal_with(employee_fields)
    def delete(self, employee_id):
        error: str = delete_employee_by_id(employee_id)
        if error is not None:
            return {'error': error}, 500
        else:
            return {}


    #updates employee
    @marshal_with(employee_fields)  # serialization of the returned object to json)
    def put(self, employee_id):  # add employee
        args: dict = employee_parse_args.parse_args()  # returns employee dict from flask request
        error, employee = update_employee_or_error(employee_id, args)
        if error is not None:
            return {'error': error}, 500
        return employee


class DepartmentEmployee(Resource):
    @marshal_with(employee_fields)  # serialization of the returned object to json()
    def get(self, department_id):
        return get_employees_by_department_id(department_id)


    # creates employee
    @marshal_with(employee_fields)  # serialization of the returned object to json)
    def post(self, department_id):  # add employee
        args: dict = employee_parse_args.parse_args()  # returns employee dict from flask request
        (error, employee) = create_employee_or_error(args)
        if error is not None:
            return {'error': error}, 500
        return employee
