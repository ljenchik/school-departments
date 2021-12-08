from datetime import datetime
from flask import render_template, request
from department_app import app


@app.route('/search-employee')
def search_employee_get():
    birthdate = ''
    if 'dob' in request.args:
        birthdate = request.args['dob']
    return render_template('employee_search.html', date_of_birth =birthdate)

# /api/employee/dob/2020-01-01
# /api/employee/from/2020-01-01/to/0987-09-08

# /api/employee/search?dob=2020-01-01
# /api/employee/search?from=2020-01-01&to=6543-09-09