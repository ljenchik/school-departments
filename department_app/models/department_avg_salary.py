"""
Department model used to represent departments with average salaries,
this module defines the following classes:
- `DepartmentAvgSalary`, department model
"""

from datetime import datetime

from department_app import db


class DepartmentAvgSalary(db.Model):
    """
            Model representing department
            :param str name: name of the department
            :param float avg_salary: average salary of the department
    """
    #: Database id of the department
    id = db.Column(db.Integer, primary_key=True)
    #: Name of the department
    name = db.Column(db.String(200), nullable=False, unique=True)
    #: Date when the department was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #: Average salary of department
    avg_salary = db.Column(db.Float)
    #: Name of the database table storing departments with average salary
    __tablename__ = 'Department_Avg_Salary_ignore'

    def __repr__(self):
        return f'<Department_avg_salary {self.id}'
