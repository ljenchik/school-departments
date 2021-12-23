"""
This package contains modules department_rest_api.py and employee_rest_api.py
"""
from flask_restful import Api

from department_app import app
from department_app.rest.department_rest_api import DepartmentWithSalary, Department
from department_app.rest.employee_rest_api import Employee, DepartmentEmployee, SearchEmployee

api = Api(app)
api.add_resource(DepartmentWithSalary, '/api/departments')
api.add_resource(Department, '/api/departments/<int:department_id>')
api.add_resource(Employee, '/api/employee/<int:employee_id>')
api.add_resource(DepartmentEmployee, '/api/department/<int:department_id>/employee')
api.add_resource(SearchEmployee, '/api/employee/search')
