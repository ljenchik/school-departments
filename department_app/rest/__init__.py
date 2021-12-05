from flask_restful import Api

from department_app import app
from .department_rest_api import DepartmentWithSalary, Department
from .employee_rest_api import Employee, DepartmentEmployee

api = Api(app)
api.add_resource(DepartmentWithSalary, '/api/departments')
api.add_resource(Department, '/api/departments/<int:department_id>')
api.add_resource(Employee, '/api/employee/<int:employee_id>')
api.add_resource(DepartmentEmployee, '/api/department/<int:department_id>/employee')