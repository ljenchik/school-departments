from datetime import datetime

import flask
import requests
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from werkzeug.exceptions import abort
from models.department import Department
from models.db_shared import db
from models.employee import Employee

from rest_api import DepartmentWithSalary, Department

from service.department_service import create_department_or_error, get_department_by_id, \
    update_department

from service.employee_service import create_employee_or_error, update_employee, validate_employee, parse_float, \
    delete_employee_by_id

from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/dep'
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
api.add_resource(DepartmentWithSalary, '/api/department')
api.add_resource(Department, '/api/department/<int:department_id>')

@app.route('/', methods = ['POST', 'GET'])
def index_department():
    if request.method == 'POST':
        department_id = request.form['id']
        error = requests.delete(flask.request.url_root + f'api/department/{department_id}')
        if error is not None:
            departments = requests.get(flask.request.url_root + 'api/department').json()
            return render_template('departments.html', departments=departments, error=error)

    departments = requests.get(flask.request.url_root + 'api/department').json()
    return render_template('departments.html', departments=departments, error = '')


@app.route('/department/add', methods=['POST', 'GET'])
def add_department():
    if request.method == 'POST':
        department_name = request.form['name']
        new_department = Department(name=department_name.strip())
        if new_department.name == '':
            return render_template('department.html', dep=new_department,
                                   error='Please enter new department')
        error = create_department_or_error(new_department)
        if error is not None:
            return render_template('department.html', dep=new_department,
                                   error=error)
        return redirect('/')
    else:
        new_department = Department(name='')
        return render_template('department.html', dep=new_department, error='')


def get_or_404(model):
    if model is None:
        abort(404)
    return model


@app.route('/department/edit/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    dep_to_edit = get_or_404(get_department_by_id(id))
    if request.method == 'POST':
        error = update_department(dep_to_edit, request.form['name'])
        if error is not None:
            return render_template('department.html', dep=dep_to_edit, error=error)
        return redirect('/')
    else:
        return render_template('department.html', dep=dep_to_edit, error = '')


@app.route('/department/<int:department_id>/employees', methods = ['POST', 'GET'])
def index_employee(department_id):
    dep = requests.get(flask.request.url_root + f'api/department/{department_id}').json()
    if request.method == 'POST':
        employee_id = request.form['id']
        error = delete_employee_by_id(employee_id)
        if error is not None:
            employees = Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()
            return render_template('employees.html', employees=employees, department=dep, error = error)

    employees = Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()
    return render_template('employees.html', employees=employees, department=dep, error = '')


@app.route('/add-employee/<int:department_id>', methods=['POST', 'GET'])
def add_employee(department_id):
    if request.method == 'POST':
        dep = Department.query.get_or_404(department_id)
        new_employee = Employee(department_id=department_id)
        fill_employee_from_request(new_employee)
        validation_error = validate_employee(new_employee)
        if validation_error is not None:
            return render_template('employee.html', employee=new_employee, department_name=dep.name,
                                   department_id=department_id, error=validation_error)
        error = create_employee_or_error(new_employee)
        if error is not None:
            return render_template('employee.html', employee=new_employee, department_name=dep.name,
                                   department_id=department_id, error=error)
        return redirect(f'/department/{department_id}/employees')
    else:
        dep = Department.query.get_or_404(department_id)
        employee = Employee(name='', role='', salary='', start_date=datetime.today())
        return render_template('employee.html', employee=employee, department_name=dep.name,
                               department_id=dep.id, error='')


def fill_employee_from_request(new_employee):
    new_employee.name = request.form['name']
    new_employee.role = request.form['role']
    new_employee.date_of_birth = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
    new_employee.salary = parse_float(request.form['salary'])
    new_employee.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')


@app.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    emp_to_edit = Employee.query.get_or_404(employee_id)
    dep = Department.query.get_or_404(emp_to_edit.department_id)

    if request.method == 'POST':
        fill_employee_from_request(emp_to_edit)
        error = update_employee(emp_to_edit, emp_to_edit.name, emp_to_edit.role, emp_to_edit.date_of_birth,
                                emp_to_edit.salary, emp_to_edit.start_date)
        if error is not None:
            return render_template('employee.html', employee=emp_to_edit, department_name=dep.name,
                                   department_id=dep.id, error=error)
        return redirect(f'/department/{emp_to_edit.department_id}/employees')
    else:
        return render_template('employee.html', employee=emp_to_edit, department_name=dep.name, department_id=dep.id,
                               error='')



if __name__ == "__main__":
    app.run(debug=True)
