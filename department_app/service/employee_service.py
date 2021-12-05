from datetime import datetime

from department_app import db
from department_app.models.employee import Employee

def get_employees_by_department_id(department_id:int):
    return Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()

def create_employee_or_error(args: dict) -> (str, Employee):
    new_employee:Employee = Employee(
        # name=args['name'],
        # role=args['role'],
        # date_of_birth=args['date_of_birth'],
        # salary=args['salary'],
        # start_date=args['start_date'],
        # department_id=args['department_id']
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


def validate_employee(emp: dict) -> str:
    start_date:datetime = emp['start_date']
    dob:datetime  = emp['date_of_birth']
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

