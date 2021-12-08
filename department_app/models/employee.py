"""
Employee model used to represent employees, this module defines the
following classes:
- `Employee`, employee model
"""

from datetime import datetime

from sqlalchemy import ForeignKey

from department_app import db
from .department import Department


class Employee(db.Model):
    """
       Model representing employee
       :param str name: employee's name
       :param str role: employee's role
       :param date date_of_birth: employee's date of birth
       :param float salary: employee's salary
       :param start_date: date when employee started work
       :type department: Department or None

       """
    #: employee's database id
    id = db.Column(db.Integer, primary_key=True)
    #: employee's department id
    department_id = db.Column(db.Integer, ForeignKey(Department.id), nullable=False)
    #: date when employee's record was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #: employee's name
    name = db.Column(db.String(200), nullable=False)
    #: employee's role
    role = db.Column(db.String(100))
    #: employee's date of birth
    date_of_birth = db.Column(db.DateTime)
    #: employee's salry
    salary = db.Column(db.Float)
    #: employee's start date
    start_date = db.Column(db.DateTime)

    def __init__(self, name, role,  date_of_birth, salary, start_date, department=None):
        #: employee's name
        self.name = name

        #: employee's role
        self.role = role

        #: employee's date of birth
        self.date_of_birth = date_of_birth

        #: employee's salary
        self.salary = salary

        #: employee's start_date
        self.start_date = start_date

        #: department employee works in
        self.department = department

    def __repr__(self):
        """
        Returns string representation of employee
        :return: string representation of employee
        """
        return f'<Employee {self.id!r}>'





