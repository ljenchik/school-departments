"""
Employee model represents employee with class Employee
"""

from datetime import datetime

from sqlalchemy import ForeignKey

from department_app import db
from .department import Department

# pylint: disable=too-many-instance-attributes
class Employee(db.Model):
    """
    Model representing employee
    :param str 'name': employee's name
    :param str 'role': employee's role
    :param date 'date_of_birth': employee's date of birth
    :param float 'salary': employee's salary
    :param date 'start_date': date when employee started work
    :type 'department': Department or None
    """
    # pylint: disable=too-few-public-methods
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
    #: employee's salary
    salary = db.Column(db.Float)
    #: employee's start date
    start_date = db.Column(db.DateTime)

    def __repr__(self):
        """
        Returns string representation of employee
        :return: string representation of employee
        """
        return f'Employee {self.id}'
