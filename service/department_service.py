from models.db_shared import db
from models.department import Department
from models.department_avg_salary import DepartmentAvgSalary


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


def create_department_or_error(name:str) -> str:
    new_department = Department(name = name)
    try:
        db.session.add(new_department)
        db.session.commit()
        return (None, new_department)
    except Exception as e:
        db.session.rollback()
        error = str(e)
        if 'Duplicate' in error:
            error = 'Department with this name already exists'
        return (error, None)


def get_department_by_id(id: int) -> Department:
    department = Department.query.get(id)
    return department


def update_department(department_id: int, name: str):
    department = get_department_by_id(department_id)
    department.name = name
    if name.strip() == '':
        return 'Please enter department name'
    try:
        db.session.commit()
    except:
        return 'There is an issue with editing this department'


def delete_department_by_id(id: int):
    dep_to_delete = get_department_by_id(id)
    try:
        db.session.delete(dep_to_delete)
        db.session.commit()
    except:
        db.session.rollback()
        return 'You cannot delete department with employees'
