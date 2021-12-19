from datetime import datetime

import flask
import requests
from flask import render_template, request
from department_app import app


def get_url(url: str):
    return flask.request.url_root + url


@app.route('/search-employee')
def search_employee_get():
    birthdate = ''
    date_from = ''
    date_to = ''
    employees:list = None
    if 'dob' in request.args:
        birthdate = request.args['dob']
        employees = requests.get(get_url(f'/api/employee/search?date_of_birth={birthdate}')).json()
    elif 'date_from' in request.args and 'date_to' in request.args:
        date_from = request.args['date_from']
        date_to = request.args['date_to']
        employees = requests.get(get_url(f'/api/employee/search?date_from={date_from}&date_to={date_to}')).json()
    return render_template('employee_search.html', date_of_birth=birthdate, date_from=date_from, date_to=date_to,
                           employees=employees)

