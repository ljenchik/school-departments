"""
Department with average salaries model is represented by class DepartmentAvgSalary
"""

from datetime import datetime

from department_app import db


class DepartmentAvgSalary(db.Model):
    """
    Model representing department
    """
    # pylint: disable=too-few-public-methods
    #: Database department id
    id = db.Column(db.Integer, primary_key=True)
    #: Department name
    name = db.Column(db.String(200), nullable=False, unique=True)
    #: Date when the department was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #: Average salary of the department
    avg_salary = db.Column(db.Float)
    #: Name of the database table storing departments with average salary
    __tablename__ = 'Department_Avg_Salary_ignore'

    def __repr__(self):
        return f'Department_avg_salary {self.id}'
