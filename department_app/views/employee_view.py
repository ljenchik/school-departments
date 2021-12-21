from datetime import datetime
from json import JSONDecodeError

import flask
import requests
from flask import render_template, request, redirect
from werkzeug.exceptions import abort

from department_app import app


def get_url(url: str):
    return flask.request.url_root + url


# displays the list of employees of the chosen department
@app.route('/department/<int:department_id>/employees')
def index_employee(department_id: str):
    dep = get_department_by_id(department_id)
    # get employees by department id
    search_or_department = 'Departments'
    reffer = request.referrer
    if reffer is None:
        reffer = '/'

    if 'search-employee' in reffer:
        search_or_department = 'Search'

    employees: list = requests.get(get_url(f'/api/department/{department_id}/employee')).json()
    return render_template('employees.html', employees=employees, department=dep, error='',
                           reffer = reffer, backlink_name = search_or_department)


# deletes employee
@app.route('/department/<int:department_id>/employees', methods=['POST'])
def delete_employee(department_id: str):
    dep = get_department_by_id(department_id)
    employee_id = request.form['id']
    error_dict: dict = requests.delete(get_url(f'/api/employee/{employee_id}')).json()
    if len(error_dict) != 0:
        employees = requests.get(get_url(f'/api/department/{department_id}/employee')).json()
        return render_template('employees.html', employees=employees, department=dep, error=error_dict)
    return redirect(f'/department/{department_id}/employees')


def get_department_by_id(department_id: str) -> dict:
    response = requests.get(flask.request.url_root + f'api/departments/{department_id}')
    if response.status_code == 200:
        return response.json()
    else:
        abort(response.status_code)  # raise exception


@app.route('/add-employee/<int:department_id>', methods=['POST'])
def add_employee_post(department_id: str):
    dep: dict = get_department_by_id(department_id)
    new_employee: dict = fill_employee_from_request()
    new_employee['department_id'] = int(department_id)
    response = requests.post(
        flask.request.url_root + f'/api/department/{department_id}/employee',
        data=new_employee
    )
    if response.status_code == 200:
        return redirect(f'/department/{department_id}/employees')

    error_text = f'REST API Error. Response code: {response.status_code}. {response.text}'
    try:
        error_or_employee: dict = response.json()
        if 'error' in error_or_employee:
            error_text = error_or_employee['error']
    except JSONDecodeError:
        pass

    new_employee['id'] = None
    return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                           department_id=department_id, error=error_text)


@app.route('/add-employee/<int:department_id>')
def add_employee_get(department_id:str):
    new_employee: dict = {"name": '', 'id': None, 'role': '',
                          'date_of_birth': None, 'salary': '', 'start_date': datetime.today().strftime('%Y-%m-%d')}
    dep: dict = get_department_by_id(department_id)
    return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                           department_id=dep['id'], error='')


def parse_float(value):
    return float(value.replace(" ", "").replace(",", ""))


def fill_employee_from_request():
    new_employee = {'department_id': request.form['department_id'], 'name': request.form['name'],
                    'role': request.form['role'], 'date_of_birth': request.form['birthdate'],
                    'salary': parse_float(request.form['salary']), 'start_date': request.form['start_date']}
    return new_employee


@app.route('/edit-employee/<int:employee_id>', methods=['POST'])
def edit_employee_put(employee_id):
    employee_to_edit: dict = fill_employee_from_request()
    employee_to_edit['id'] = employee_id
    department_id = employee_to_edit['department_id']
    response = requests.put(flask.request.url_root + f'/api/employee/{employee_id}', data=employee_to_edit)

    if response.status_code == 200:
        return redirect(f'/department/{department_id}/employees')

    error_text = f'REST API status code: {response.status_code}. Message: {response.text}'
    try:
        error_or_employee: dict = response.json()
        if 'error' in error_or_employee:
            error_text: str = error_or_employee['error']
    except JSONDecodeError:
        pass

    dep: dict = get_department_by_id(department_id)
    return render_template('employee.html', employee=employee_to_edit, department_name=dep['name'],
                           department_id=dep['id'], error=error_text)


def get_employee_by_id(employee_id: str) -> dict:
    response = requests.get(flask.request.url_root + f'api/employee/{employee_id}')
    if response.status_code == 200:
        return response.json()
    else:
        abort(response.status_code)  # raise exception


@app.route('/edit-employee/<int:employee_id>')
def edit_employee_get(employee_id):
    employee_to_edit: dict = get_employee_by_id(employee_id)
    dep: dict = get_department_by_id(employee_to_edit['department_id'])
    return render_template('employee.html', employee=employee_to_edit, department_name=dep['name'],
                           department_id=dep['id'], error='')
