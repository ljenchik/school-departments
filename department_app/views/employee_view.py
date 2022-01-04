"""
Employee Flask views
"""
# pylint: disable=cyclic-import
import http
from datetime import datetime
from json import JSONDecodeError

import flask
import requests
from flask import render_template, request, redirect
from werkzeug.exceptions import abort

from department_app import app


def get_url(url: str):
    """
    creates rest api url
    :param url:
    :return: absolute rest api url
    """
    return flask.request.url_root + url


@app.route('/department/<int:department_id>/employees')
def index_employee(department_id: str):
    """
    displays the list of employees of the chosen department
    :param department_id
    :return: rendered template
    """
    dep: dict = get_department_by_id(department_id)
    # get employees by department id
    referer = request.referrer
    if referer is None or 'search-employee' not in referer:
        referer = None

    employees: list = requests.get(get_url(f'/api/department/{department_id}/employee')).json()
    return render_template('employees.html', employees=employees, department=dep, error='',
                           reffer=referer)


@app.route('/department/<int:department_id>/employees', methods=['POST'])
def delete_employee(department_id: str):
    """
    deletes employee
    :param department_id:
    :return: rendered template or redirect to department employees
    """
    dep = get_department_by_id(department_id)
    employee_id = request.form['id']
    response = requests.delete(get_url(f'/api/employee/{employee_id}'))
    error_text = handle_rest_response(response)
    if error_text is None:
        return redirect(f'/department/{department_id}/employees')

    employees = requests.get(get_url(f'/api/department/{department_id}/employee')).json()
    return render_template('employees.html', employees=employees, department=dep,
                           error=error_text)


def handle_rest_response(response):
    """
    checks rest api http response code and tries to get error text from the response
    :param response:
    :return: None is response is successful, error otherwise
    """
    error_text = None
    if response.status_code != http.HTTPStatus.OK:
        error_text = f'REST API Error. Response code: {response.status_code}. {response.text}'
        try:
            error_or_employee: dict = response.json()
            if 'error' in error_or_employee:
                error_text = error_or_employee['error']
        except JSONDecodeError:
            pass
    return error_text


def get_department_by_id(department_id: str) -> dict:
    """
    gets departments by its id
    :param department_id:
    :return: department from rest api as dictionary
    """
    response = requests.get(flask.request.url_root + f'api/departments/{department_id}')
    if response.status_code == http.HTTPStatus.OK:
        return response.json()
    abort(response.status_code)  # raise exception
    return None


@app.route('/add-employee/<int:department_id>', methods=['POST'])
def add_employee_post(department_id: str):
    """
    adds employee
    :param department_id:
    :return: redirects to department employees
    """
    dep: dict = get_department_by_id(department_id)
    new_employee: dict = fill_employee_from_request()
    new_employee['department_id'] = int(department_id)
    response = requests.post(
        flask.request.url_root + f'/api/department/{department_id}/employee',
        json=new_employee
    )
    error_text = handle_rest_response(response)
    if error_text is None:
        return redirect(f'/department/{department_id}/employees')

    new_employee['id'] = None
    return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                           department_id=department_id, error=error_text)


@app.route('/add-employee/<int:department_id>')
def add_employee_get(department_id: str):
    """
    gets new employee form
    :param department_id:
    :return: rendered template
    """
    new_employee: dict = {"name": '', 'id': None, 'role': '',
                          'date_of_birth': None, 'salary': '',
                          'start_date': datetime.today().strftime('%Y-%m-%d')}
    dep: dict = get_department_by_id(department_id)
    return render_template('employee.html', employee=new_employee, department_name=dep['name'],
                           department_id=dep['id'], error='')


def parse_float(value):
    """
    parses float from string
    :param value:
    :return: float
    """
    return float(value.replace(" ", "").replace(",", ""))


def fill_employee_from_request():
    """
    fills employee from request form
    :return: new employee as dictionary
    """
    new_employee = {'department_id': request.form['department_id'], 'name': request.form['name'],
                    'role': request.form['role'], 'date_of_birth': request.form['birthdate'],
                    'salary': parse_float(request.form['salary']),
                    'start_date': request.form['start_date']}
    return new_employee


@app.route('/edit-employee/<int:employee_id>', methods=['POST'])
def edit_employee_put(employee_id):
    """
    edits employee
    :param employee_id:
    :return: redirects to department employees
    """
    employee_to_edit: dict = fill_employee_from_request()
    employee_to_edit['id'] = employee_id
    department_id = employee_to_edit['department_id']
    response = requests.put(flask.request.url_root +
                            f'/api/employee/{employee_id}', json=employee_to_edit)

    error_text = handle_rest_response(response)
    if error_text is None:
        return redirect(f'/department/{department_id}/employees')

    dep: dict = get_department_by_id(department_id)
    return render_template('employee.html', employee=employee_to_edit, department_name=dep['name'],
                           department_id=dep['id'], error=error_text)


def get_employee_by_id(employee_id: str) -> dict:
    """
    gets employee by her/his id
    :param employee_id:
    :return: employee as dictionary
    """
    response = requests.get(flask.request.url_root + f'api/employee/{employee_id}')
    if response.status_code == http.HTTPStatus.OK:
        return response.json()
    abort(response.status_code)  # raise exception
    return None


@app.route('/edit-employee/<int:employee_id>')
def edit_employee_get(employee_id):
    """
    gets employee by her/his id
    :param employee_id:
    :return: rendered template
    """
    employee_to_edit: dict = get_employee_by_id(employee_id)
    dep: dict = get_department_by_id(employee_to_edit['department_id'])
    return render_template('employee.html', employee=employee_to_edit, department_name=dep['name'],
                           department_id=dep['id'], error='')
