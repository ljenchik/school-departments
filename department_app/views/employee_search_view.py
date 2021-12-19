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
    employees:list = None
    if 'dob' in request.args:
        birthdate = request.args['dob']
        employees = requests.get(get_url(f'/api/employee/search?date_of_birth={birthdate}')).json()
    return render_template('employee_search.html', date_of_birth=birthdate, employees = employees)



# /api/employee/search?from=2020-01-01&to=6543-09-09
# https://stackoverflow.com/questions/30779584/flask-restful-passing-parameters-to-get-request