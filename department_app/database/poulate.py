"""
This module is used to populate database with departments and employees,
it defines the following:
Functions:
- `populate_database`: populate database with employees and departments
"""

from datetime import date

from department_app import db
from department_app.models.department import Department
from department_app.models.employee import Employee


def populate_database():
    """
    Populate database with employees and departments
    :return: None
    """
    department_1 = Department('Department of Mathematics')
    department_2 = Department('Department of Sciences')
    department_3 = Department('Department of Modern Foreign Languages')

    employee_1 = Employee('Karen Wilbourne', 'Head of department',
                          date(1987, 4, 12), 42000, '01/09/2016')
    employee_2 = Employee('Mark Brown', 'Science teacher',
                          date(1980, 2, 23), 38450, '01/09/2005')
    employee_3 = Employee('Tracey Smith', 'Spanish teacher',
                          date(1989, 5, 30), 37863.2, '01/09/2019')

    department_1.employees = [employee_1]
    department_2.employees = [employee_2]
    department_3.employees = [employee_3]

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)

    db.session.add(employee_1)
    db.session.add(employee_2)
    db.session.add(employee_3)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating database...')
    populate_database()
    print('Successfully populated')
