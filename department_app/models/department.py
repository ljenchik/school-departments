"""
Department model used to represent departments, this module defines the
following classes:
- `Department`, department model
"""

from department_app import db
from datetime import datetime


class Department(db.Model):
    """
        Model representing department
        :param str name: name of the department
        """

    #: Database id of the department
    id = db.Column(db.Integer, primary_key=True)
    #: Name of the department
    name = db.Column(db.String(200), nullable=False, unique=True)
    #: Date when the department was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        Returns string representation of department
        """
        return f'Department({self.name}, {self.id})'


