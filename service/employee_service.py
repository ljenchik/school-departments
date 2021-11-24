from datetime import datetime
from dateutil.relativedelta import relativedelta
from models.db_shared import db
from models.employee import Employee


def create_employee_or_error(new_employee: Employee):
    try:
        db.session.add(new_employee)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return 'There was an issue adding a new employee ' + str(e)


def update_employee(employee: Employee, name:str, role, date_of_birth, salary, start_date):
    employee.name = name
    employee.role = role
    employee.date_of_birth = date_of_birth
    employee.salary = salary
    employee.start_date = start_date
    error = validate_employee(employee)
    if error is not None:
        return error
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return 'There was an issue editing an employee: ' + str(e)


def validate_employee(emp: Employee) -> str:
    if relativedelta(emp.start_date, emp.date_of_birth).years < 18:
        return 'Employee must be at least 18 to start work'
    if datetime.today().year - emp.date_of_birth.year > 100:
        return "Please check employee's date of birth"


def parse_float(value):
    return float((value).replace(" ", "").replace(",", ""))