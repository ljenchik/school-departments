from datetime import datetime

import flask
import requests
from flask import render_template, request, redirect
from werkzeug.exceptions import abort

from department_app import app


def get_url(url: str):
    return flask.request.url_root + url


# displays the list of employees of the chosen department
@app.route('/department/<int:department_id>/employees')
def index_employee(department_id: int):
    dep = get_department_by_id(department_id)
    # get employees by department id
    employees: list = requests.get(get_url(f'/api/department/{department_id}/employee')).json()
    return render_template('employees.html', employees=employees, department=dep, error='')


# deletes employee
@app.route('/department/<int:department_id>/employees', methods=['POST'])
def delete_employee(department_id: int):
    dep = get_department_by_id(department_id)
    employee_id = request.form['id']
    error_dict: dict = requests.delete(get_url(f'/api/employee/{employee_id}')).json()
    if len(error_dict) != 0:
        employees = requests.get(get_url(f'/api/department/{department_id}/employee')).json()
        return render_template('employees.html', employees=employees, department=dep, error=error_dict)
    return redirect(f'/department/{department_id}/employees')


def get_department_by_id(department_id: str) -> dict:
    response: request.Response = requests.get(flask.request.url_root + f'api/departments/{department_id}')
    if response.status_code == 200:
        return response.json()
    else:
        abort(response.status_code)  # raise exception


@app.route('/add-employee/<int:department_id>', methods=['POST', 'GET'])
def add_employee(department_id:str):
    if request.method == 'POST':  # when click save button
        dep: dict = get_department_by_id(department_id)
        new_employee: dict = fill_employee_from_request()
        new_employee['department_id'] = int(department_id)
        response: request.Response = requests.post(flask.request.url_root + f'/api/department/{department_id}/employee', data=new_employee)
        if response.status_code == 200:
            return redirect(f'/department/{department_id}/employees')

        error_text = f'REST API Error. Response code: {response.status_code}. {response.text}'
        error_or_employee: dict = response.json()
        if 'error' in error_or_employee:
            error_text = error_or_employee['error']

        new_employee['id'] = None
        return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                               department_id=department_id, error=error_text)

    else:
        new_employee: dict = {"name": '', 'id': None, 'role': '',
                              'date_of_birth': None, 'salary': '', 'start_date': datetime.today()}
        dep: dict = get_department_by_id(department_id)
        return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                               department_id=dep['id'], error='')


def parse_float(value):
    return float((value).replace(" ", "").replace(",", ""))


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
