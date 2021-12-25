"""
Employee_search Flask view
"""

import flask
import requests
from flask import render_template, request
from department_app import app


def get_url(url: str):
    """
    creates rest api url
    :param url:
    :return: absolute rest api url
    """
    return flask.request.url_root + url


@app.route('/search-employee')
def search_employee_get():
    """
    gets employees born on given date or over a period between two dates
    :return: rendered template
    """
    birthdate = ''
    date_from = ''
    date_to = ''
    employees: list = None
    if 'dob' in request.args:
        birthdate = request.args['dob']
        employees = requests.get(get_url(f'/api/employee/search?date_of_birth={birthdate}')).json()
        return render_template('employee_search.html', date_of_birth=birthdate,
                               employees=employees)
    if 'date_from' in request.args and 'date_to' in request.args:
        date_from = request.args['date_from']
        date_to = request.args['date_to']
        employees = requests.get(
            get_url(
                f'/api/employee/search?date_from={date_from}&date_to={date_to}')).json()
    return render_template('employee_search.html', date_from=date_from,
                           date_to=date_to, employees=employees)
