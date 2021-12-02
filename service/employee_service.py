from datetime import datetime
from dateutil.relativedelta import relativedelta
from models.db_shared import db
from models.employee import Employee


def create_employee_or_error(args: dict) -> (str, Employee):
    new_employee = Employee(
        # name=args['name'],
        # role=args['role'],
        # date_of_birth=args['date_of_birth'],
        # salary=args['salary'],
        # start_date=args['start_date'],
        # department_id=args['department_id']
        **args
    )

    try:
        db.session.add(new_employee)
        db.session.commit()
        return None, new_employee
    except Exception as e:
        db.session.rollback()
        return 'There was an issue adding a new employee ' + str(e), None


def update_employee(employee: Employee, name: str, role, date_of_birth, salary, start_date):
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


def delete_employee_by_id(employee_id):
    emp_to_delete = Employee.query.get_or_404(employee_id)
    try:
        db.session.delete(emp_to_delete)
        db.session.commit()
    except:
        db.session.rollback()
        return 'There was an issue deleting this employee'
