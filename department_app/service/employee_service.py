"""
Employee service is used to make database queries
"""
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from department_app import db
from department_app.models.employee import Employee
from department_app.models.employee_with_department_name import EmployeeDepName


def get_employees_by_department_id(department_id: int):
    """
    get employees working in the department given by its id
    :param department_id:
    :return: list of employees
    """
    return db.session.query(Employee).filter_by(
        department_id=department_id).order_by(Employee.date_created).all()

def create_employee_or_error(args: dict) -> (str, Employee):
    """
    adds and validates new employee
    :param args:
    :return: tuple (error, new employee)
    """
    new_employee: Employee = Employee(
        **args
    )
    error = validate_employee(args)
    if error is not None:
        return error, None
    try:
        db.session.add(new_employee)
        db.session.commit()
        return None, new_employee
    except SQLAlchemyError as error:
        db.session.rollback()
        return 'There was an issue adding a new employee ' + str(error), None


def update_employee_or_error(employee_id: int, employee_dict: dict) -> (str, Employee):
    """
    updates employee's data
    :param employee_id:
    :param employee_dict:
    :return: tuple (error, updated employee)
    """
    error = validate_employee(employee_dict)
    if error is not None:
        return error, None

    employee: Employee = get_employee_by_id(employee_id)
    employee.name = employee_dict['name']
    employee.role = employee_dict['role']
    employee.date_of_birth = employee_dict['date_of_birth']
    employee.salary = employee_dict['salary']
    employee.start_date = employee_dict['start_date']

    try:
        db.session.commit()
        return None, employee
    except SQLAlchemyError as error:
        db.session.rollback()
        return 'There was an issue editing an employee: ' + str(error), None


def validate_employee(emp: dict) -> str:
    """
    validates birth dates and start dates
    :param emp:
    :return: error
    """
    start_date: datetime = emp['start_date']
    dob: datetime = emp['date_of_birth']
    if dob >= datetime.today() or dob.year >= start_date.year:
        return "Please check employee's date of birth"
    if start_date.year - dob.year < 18:
        return 'Employee must be at least 18 to start work'
    if datetime.today().year - dob.year > 100:
        return "Please check employee's date of birth"
    return None


def delete_employee_by_id(employee_id):
    """
    deletes employee by her/his given id
    :param employee_id:
    :return: None or error
    """
    emp_to_delete = Employee.query.get_or_404(employee_id)
    try:
        db.session.delete(emp_to_delete)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'There was an issue deleting this employee'
    return None


def get_employee_by_id(employee_id: int) -> Employee:
    """
    gets employee by her/his given id
    :param employee_id:
    :return: employee
    """
    employee_to_edit = db.session.query(Employee).get(employee_id)
    return employee_to_edit


def get_employee_by_dob(dob: str) -> list:
    """
    gets a list of employees born on given date of birth (dob)
    :param dob:
    :return: list of employees
    """
    employee_list = db.session.query(EmployeeDepName).from_statement(
        db.text(f"""
        SELECT e.name, e.role, e.date_of_birth, e.salary, 
            e.start_date, e.department_id, e.id, d.name as department_name 
            FROM employee e
            INNER JOIN department d 
            ON e.department_id = d.id
            WHERE date_of_birth = '{dob}'
        """)).all()
    return employee_list


def get_employee_by_period(date_from: str, date_to: str) -> list:
    """
    gets a list of employees born between two given dates
    :param date_from:
    :param date_to:
    :return: list of employees
    """
    employee_list = db.session.query(EmployeeDepName).from_statement(
        db.text(f"""
            SELECT e.name, e.role, e.date_of_birth, e.salary, 
            e.start_date, e.department_id, e.id, d.name as department_name 
            FROM employee e
            INNER JOIN department d 
            ON e.department_id = d.id
            WHERE date_of_birth >= '{date_from}' and date_of_birth <= '{date_to}'
            """)).all()
    return employee_list
