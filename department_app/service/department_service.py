from department_app import db
from department_app.models.department import Department
from department_app.models.department_avg_salary import DepartmentAvgSalary


def read_departments_with_salaries() -> list:
    departments = DepartmentAvgSalary.query.from_statement(
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
    new_department = Department(name=name)
    try:
        db.session.add(new_department)
        db.session.commit()  # saves to db
        return (None, new_department)
    except Exception as e:
        db.session.rollback()
        error = str(e)  # exception string from Python
        if 'Duplicate' in error:  # checks if department with the same name exists (unique in db)
            error = 'Department with this name already exists'
        return (error, None)  # returns tuple (error, department)


def get_department_by_id(department_id: int) -> Department:
    department = Department.query.get(department_id)
    return department


def update_department(department_id: int, name: str) -> (str, Department):
    department: Department = get_department_by_id(department_id)
    department.name = name
    if name.strip() == '':
        return ('Please enter department name', None)
    try:
        db.session.commit()
        return (None, department)
    except Exception as error:
        db.session.rollback()
        error: str = str(error)
        if 'Duplicate' in error:
            error = 'Department with this name already exists'
        return (error, None)


# returns error or None
def delete_department_by_id(department_id: int):
    dep_to_delete = get_department_by_id(department_id)
    try:
        db.session.delete(dep_to_delete)  # deletes from db
        db.session.commit()  # saves changes to db
        return None
    except:
        db.session.rollback()
        return 'You cannot delete department with employees'  # returns error if department has employees
