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
from service.employee_service import create_employee_or_error, update_employee, validate_employee, parse_float, delete_employee_by_id
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/dep'
db.init_app(app)
migrate = Migrate(app, db)


api = Api(app)
api.add_resource(DepartmentWithSalary, '/api/departments')
api.add_resource(Department, '/api/departments/<int:department_id>')

# if user goes to the url / function will be executed
# deletes department by id and displays all departments
@app.route('/', methods=['POST', 'GET'])
def index_department():
    error_text:str = '' # reuse this variable for two cases: empty string as an error and error from request to rest api
    if request.method == 'POST':
        department_id:str = request.form['id']  # requests department id from template departments.html
        # returns dictionary, empty {} or {'error' : error_text}
        error_dict:dict = requests.delete(flask.request.url_root + f'api/departments/{department_id}').json()
        if len(error_dict) != 0:
            error_text:str = error_dict['error']
    departments = requests.get(flask.request.url_root + 'api/departments').json()
    # renders templates from departments.html
    return render_template('departments.html', departments=departments, error=error_text)


# if user goes to the url /department/add the add_department() function must be executed
@app.route('/department/add', methods=['POST', 'GET'])
def add_department():
    if request.method == 'POST':
        # requests form from template department.html and enter a new department name
        department_name = request.form['name']
        dict_department_name = {'name': department_name}
        # Makes request to rest api to add new department
        error_or_department = requests.post(flask.request.url_root + f'api/departments',
                                            data=dict_department_name).json()        # serializes class to dictionary
        if 'error' in error_or_department:
            error_text = error_or_department['error']
            if error_text is not None:
                dep = {'name': department_name, 'id': None}
                return render_template('department.html', dep=dep,
                                       error=error_text)
        return redirect('/')
    else:
        # When user clicks on add department button, renders a form from department.html template
        # with empty name and empty error to enter a new department
        new_department = {"name": '', 'id': None}
        return render_template('department.html', dep=new_department, error='')


def get_or_404(model):
    if model is None:
        abort(404)
    return model


# Python decorator that Flask provides,
# if user goes to /department/edit/<int:id> the edit_department(id) function must be executed
@app.route('/department/edit/<int:id>', methods=['GET', 'POST'])
def edit_department(id:int):
    if request.method == 'POST':
        dep_to_edit_newname = request.form['name']             # request form from template department.html and input a new department name
        dict_dep_to_edit:dict = {'name' : dep_to_edit_newname}      # dictionary is needed for json
        # Makes request to rest api to upload the department to be edited by its id
        error_or_department:dict = requests.put(flask.request.url_root + f'api/departments/{id}',         # serializes class to dictionary
                                    data=dict_dep_to_edit).json()
        if 'error' in error_or_department:
            error_text:str = error_or_department['error']
            if error_text is not None:
                dep_to_edit = {'name': dep_to_edit_newname, 'id': id}
                # Render department edit template with error_text displayed in red rectangle
                return render_template('department.html', dep=dep_to_edit,
                                   error=error_text)
        return redirect('/')                            # redirects the user to the root, list of all departments
    else:
        # When user clicks on edit, we display an edit department form from 'department.html'
        # template with the current department name
        # Makes request to rest api to load the department by id
        department_to_edit:dict = get_department_by_id(id)
        # Render department edit template, error is an empty line because
        # otherwise red error rectangle will be displayed
        return render_template('department.html', dep=department_to_edit, error='')


@app.route('/department/<int:department_id>/employees', methods=['POST', 'GET'])
def index_employee(department_id):
    dep = get_department_by_id(department_id)
    if request.method == 'POST':
        employee_id = request.form['id']
        error = delete_employee_by_id(employee_id)
        if error is not None:
            employees = Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()
            return render_template('employees.html', employees=employees, department=dep, error=error)

    employees = Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()
    return render_template('employees.html', employees=employees, department=dep, error='')


def get_department_by_id(department_id:str) -> dict:
    response:request.Response = requests.get(flask.request.url_root + f'api/departments/{department_id}')
    if response.status_code == 200:
        return response.json()
    else:
        abort(response.status_code) #raise exception


@app.route('/add-employee/<int:department_id>', methods=['POST', 'GET'])
def add_employee(department_id):
    if request.method == 'POST': # when click save button
        dep:dict = get_department_by_id(department_id)
        new_employee:dict = fill_employee_from_request()
        new_employee['department_id'] = department_id

        validation_error = validate_employee(new_employee)
        if validation_error is not None:
            return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                                   department_id=department_id, error=validation_error)
        error = create_employee_or_error(new_employee)
        if error is not None:
            return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                                   department_id=department_id, error=error)
        return redirect(f'/department/{department_id}/employees')
    else:
        new_employee:dict = {"name": '', 'id' : None, 'role': '',
                        'date_of_birth' : None, 'salary' : '', 'start_date' : datetime.today()}
        dep:dict = get_department_by_id(department_id)
        return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                               department_id=dep['id'], error='')


def fill_employee_from_request():
    new_employee = {}
    new_employee['name'] = request.form['name']
    new_employee['role'] = request.form['role']
    new_employee['date_of_birth'] = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
    new_employee['salary'] = parse_float(request.form['salary'])
    new_employee['start_date'] = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    return new_employee


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
