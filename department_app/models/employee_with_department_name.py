"""
Employee with department name model used to represent employees with department name they belong to,
 this module defines the following classes:
- `EmployeeDepName`, EmployeeDepName model
"""
from datetime import datetime

from department_app import db


class EmployeeDepName(db.Model):
    """
          Model representing employee
          :param str 'name': employee's name
          :param str 'role': employee's role
          :param date 'date_of_birth': employee's date of birth
          :param float 'salary': employee's salary
          :param date 'start_date': date when employee started work
          :param str 'department_name': department name where employee belongs to
          :type 'department': Department or None

    """
    #: employee's database id
    id = db.Column(db.Integer, primary_key=True)
    #: employee's name
    name = db.Column(db.String(200), nullable=False, unique=True)
    #: employee's role
    role = db.Column(db.String(100))
    #: employee's date of birth
    date_of_birth = db.Column(db.DateTime)
    #: employee's salary
    salary = db.Column(db.Float)
    #: employee's start date
    start_date = db.Column(db.DateTime)
    #: date when employee's record was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #: employee's department id
    department_id = db.Column(db.Integer, nullable=False)
    #: employee's department name
    department_name = db.Column(db.Integer, nullable=False)
    #: Name of the database table storing employees and their respective departments
    __tablename__ = 'Employee_with_department_name_ignore'

    def __repr__(self):
        return f'<Employee_with_department_name {id}>'
