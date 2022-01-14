"""
Department service is used to make database queries
"""
# pylint: disable=cyclic-import
from sqlalchemy.exc import SQLAlchemyError

from department_app import db
from department_app.models.department import Department
from department_app.models.department_avg_salary import DepartmentAvgSalary


def read_departments_with_salaries() -> list:
    """
    Fetches all departments with average salaries from database
    :return: list of all departments
    """
    departments = db.session.query(DepartmentAvgSalary).from_statement(
        db.text("""select d.*, avg_salary
                            from department d 
                            left join (
                                select d.id, round(avg(e.salary), 2) avg_salary
                                from department d 
                                join employee e on d.id  = e.department_id 
                                GROUP by d.id
                            ) avg_sal on avg_sal.id = d.id
                            """)
    ).all()
    return departments


def create_department_or_error(name: str) -> (str, Department):
    """
    adds new department to the database
    :return: tuple (error, new department)
    """
    new_department = Department(name=name)
    if new_department.name.strip() == '':
        error = 'Empty name'
        return error, None
    try:
        db.session.add(new_department)
        db.session.commit()  # saves to db
        return None, new_department
    except SQLAlchemyError as error:
        db.session.rollback()
        error = str(error)  # exception string from Python
        # checks if department with the same name exists (unique in db)
        if 'Duplicate' in error:
            error = 'Department with this name already exists'
        return error, None


def get_department_by_id(department_id: int) -> Department:
    """
    gets department by its id
    :param department_id:
    :return: department
    """
    department = db.session.query(Department).get(department_id)
    return department


def update_department(department_id: int, name: str) -> (str, Department):
    """
    updates department name
    :param department_id:
    :param name:
    :return: tuple (error, department)
    """
    department: Department = get_department_by_id(department_id)
    department.name = name
    if name.strip() == '':
        return 'Please enter department name', None
    try:
        db.session.commit()
        return None, department
    except SQLAlchemyError as error:
        db.session.rollback()
        error: str = str(error)
        if 'Duplicate' in error:
            error = 'Department with this name already exists'
        return error, None


# returns error or None
def delete_department_by_id(department_id: int):
    """
    deletes department by its id
    :param department_id:
    :return: None or error
    """
    dep_to_delete = get_department_by_id(department_id)
    try:
        db.session.delete(dep_to_delete)  # deletes from db
        db.session.commit()  # saves changes to db
        return None
    except SQLAlchemyError:
        db.session.rollback()
        # returns message if department has employees
        return 'You cannot delete department with employees'
