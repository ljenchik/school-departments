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


def create_department_or_error(new_department : Department) -> str:
    try:
        db.session.add(new_department)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error = str(e)
        if 'Duplicate' in error:
            error = 'Department with this name already exists'
        return error


def get_department_by_id(id : int) -> Department:
    department = Department.query.get(id)
    return department


def update_department(department, name):
     department.name = name
     try:
        db.session.commit()
     except:
        return 'There is an issue with editing this department'