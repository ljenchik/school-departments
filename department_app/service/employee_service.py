from datetime import datetime

from department_app import db
from department_app.models.employee import Employee
from department_app.models.employee_with_department_name import EmployeeDepName


def get_employees_by_department_id(department_id: int):
    return Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()


def create_employee_or_error(args: dict) -> (str, Employee):
    new_employee: Employee = Employee(
        **args
    )
    error = validate_employee(args)
    if error is not None:
        return error, None
    else:
        try:
            db.session.add(new_employee)
            db.session.commit()
            return None, new_employee
        except Exception as e:
            db.session.rollback()
            return 'There was an issue adding a new employee ' + str(e), None


def update_employee_or_error(employee_id: int, employee_dict: dict) -> (str, Employee):
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
    except Exception as e:
        db.session.rollback()
        return 'There was an issue editing an employee: ' + str(e), None


def validate_employee(emp: dict) -> str:
    start_date: datetime = emp['start_date']
    dob: datetime = emp['date_of_birth']
    if start_date.year - dob.year < 18:
        return 'Employee must be at least 18 to start work'
    if datetime.today().year - dob.year > 100:
        return "Please check employee's date of birth"
    if dob >= datetime.today():
        return "Please check employee's date of birth"


def delete_employee_by_id(employee_id):
    emp_to_delete = Employee.query.get_or_404(employee_id)
    try:
        db.session.delete(emp_to_delete)
        db.session.commit()
    except:
        db.session.rollback()
        return 'There was an issue deleting this employee'


def get_employee_by_id(employee_id: int) -> Employee:
    employee_to_edit = Employee.query.get(employee_id)
    return employee_to_edit


def get_employee_by_dob(dob: str) -> list:
    employee_list = EmployeeDepName.query.from_statement(
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
    employee_list = EmployeeDepName.query.from_statement(
        db.text(f"""
            SELECT e.name, e.role, e.date_of_birth, e.salary, 
            e.start_date, e.department_id, e.id, d.name as department_name 
            FROM employee e
            INNER JOIN department d 
            ON e.department_id = d.id
            WHERE date_of_birth >= '{date_from}' and date_of_birth <= '{date_to}'
            """)).all()
    return employee_list

