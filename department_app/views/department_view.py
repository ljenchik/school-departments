"""
Department Flask views
"""
import http
from typing import Union

import flask
import requests
from flask import render_template, request, redirect
from werkzeug.exceptions import abort

from department_app import app


def get_department_by_id(department_id: Union[str, int]) -> dict:
    """
    gets department by its id
    :param department_id:
    :return: department in JSON format or None
    """
    response: requests.Response = requests.get(
        f'{flask.request.url_root}api/departments/{department_id}')
    if response.status_code == http.HTTPStatus.OK:
        return response.json()
    abort(response.status_code)  # raise exception
    return None


# if user goes to the url '/' function will be executed
@app.route('/')
def index_department():
    """
    returns rendered `departments.html` template for url route `/`
    :return: rendered `departments.html` template
    """
    response = requests.get(flask.request.url_root + 'api/departments')
    departments = response.json()
    # renders templates from departments.html
    return render_template('departments.html', departments=departments, error='')


# deletes department by id and displays all departments
@app.route('/', methods=['POST'])
def delete_department():
    """
    renders templates from departments.html
    :return: returns empty dictionary or {'error' : error_text}
    """
    # reuse this variable for two cases: empty string as an error and error from request to rest api
    error_text: str = ''
    department_id: str = request.form['id']  # requests department id from template departments.html
    # returns dictionary, empty {} or {'error' : error_text}
    error_dict: dict = requests.delete(
        f'{flask.request.url_root}api/departments/{department_id}').json()
    if len(error_dict) != 0:
        error_text: str = error_dict['error']
    departments = requests.get(f'{flask.request.url_root}api/departments').json()
    # renders templates from departments.html
    return render_template('departments.html', departments=departments, error=error_text)


# if user goes to the url /department/add the add_department() function must be executed
@app.route('/department/add', methods=['POST', 'GET'])
def add_department():
    """
    :return: returns rendered 'departments.html' template for url route '/department/add'
    """
    if request.method == 'POST':
        # requests form from template department.html and enter a new department name
        department_name: str = request.form['department_name']
        dict_department_name: dict = {'name': department_name}
        # Makes request to rest api to add new department
        error_or_department: dict = requests.post(
            f'{flask.request.url_root}api/departments',
            json=dict_department_name).json()  # serializes class to dictionary
        if 'error' in error_or_department:
            error_text = error_or_department['error']
            if error_text is not None:
                dep = {'name': department_name, 'id': None}
                return render_template('department.html', dep=dep,
                                       error=error_text)
        return redirect('/')
    # When user clicks on add department button, renders a form from department.html template
    # with empty name and empty error to enter a new department
    new_department = {"name": '', 'id': None}
    return render_template('department.html', dep=new_department, error='')


# Python decorator that Flask provides,
# if user goes to /department/edit/<int:id> the edit_department(id) function must be executed
@app.route('/department/edit/<int:department_id>', methods=['GET', 'POST'])
def edit_department(department_id: int):
    """
    returns rendered `department.html` template for url routes
    `/department/edit/<int:department_id>`
    :param department_id:
    :return:
    """
    if request.method == 'POST':
        # request form from template department.html and input a new department name
        dep_to_edit_newname = request.form['department_name']
        dict_dep_to_edit: dict = {'name': dep_to_edit_newname}  # dictionary is needed for json
        # Makes request to rest api to upload the department to be edited by its id
        error_or_department: dict = requests.put(
            flask.request.url_root + f'api/departments/{department_id}',
            # serializes class to dictionary
            json=dict_dep_to_edit).json()
        if 'error' in error_or_department:
            error_text: str = error_or_department['error']
            if error_text is not None:
                dep_to_edit = {'name': dep_to_edit_newname, 'id': department_id}
                # Render department edit template with error_text displayed in red rectangle
                return render_template('department.html', dep=dep_to_edit, error=error_text)
        return redirect('/')  # redirects the user to the root, list of all departments
    # When user clicks on edit, we display an edit department form from 'department.html'
    # template with the current department name
    # Makes request to rest api to load the department by id
    department_to_edit: dict = get_department_by_id(department_id)
    # Render department edit template, error is an empty line because
    # otherwise red error rectangle will be displayed
    return render_template('department.html', dep=department_to_edit, error='')
