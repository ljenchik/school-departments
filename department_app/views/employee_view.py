import flask
import requests
from flask import render_template, request, redirect
from werkzeug.exceptions import abort

from department_app import app

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
