"""
This package contains department_rest_api.py and employee_rest_api.py modules
"""
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
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

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Department App',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger.json',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

docs.register(DepartmentWithSalary)
docs.register(Department)
docs.register(Employee)
docs.register(DepartmentEmployee)
docs.register(SearchEmployee)
