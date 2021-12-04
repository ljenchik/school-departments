from datetime import datetime

from flask_restful import Resource, fields, marshal_with, reqparse

from department_app.service.employee_service import create_employee_or_error

department_put_args: reqparse.RequestParser = reqparse.RequestParser()
department_put_args.add_argument('name', type=str, required=True, help='Name of department')

employee_parse_args: reqparse.RequestParser = reqparse.RequestParser()
employee_parse_args.add_argument('name', type=str, required=True, help='Name of employee')
employee_parse_args.add_argument('role', type=str, required=True, help='Role of employee')
employee_parse_args.add_argument('date_of_birth', type=datetime, required=True, help='Date of birth of employee')
employee_parse_args.add_argument('salary', type=float, required=True, help='Salary of employee')
employee_parse_args.add_argument('department_id', type=int, required=True, help='Id of department')
employee_parse_args.add_argument('start_date', type=datetime, required=True, help='Start date')

employee_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'role': fields.String,
    'date_of_birth': fields.DateTime,
    'salary': fields.Float,
    'start_date': fields.DateTime,
    'department_id': fields.Integer,
    'error': fields.String,
}


class Employee(Resource):
    @marshal_with(employee_fields)  # serialization of the returned object to json)
    def post(self):  # add employee
        args: dict = employee_parse_args.parse_args()
        (error, employee) = create_employee_or_error(args)
        if error is not None:
            return {'error': error}, 500
        return employee
