"""
Department model represents departments with class Department
"""

from datetime import datetime

from department_app import db


class Department(db.Model):
    """
    Model represents department
    """
    # pylint: disable=too-few-public-methods
    #: Database department id
    id = db.Column(db.Integer, primary_key=True)
    #: Department name
    name = db.Column(db.String(200), nullable=False, unique=True)
    #: Date when the department was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        Returns string representation of department
        """
        return f'Department({self.name}, {self.id})'
