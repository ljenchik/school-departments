from sqlalchemy import ForeignKey
from models.db_shared import db
from datetime import datetime
from models.department import Department


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, ForeignKey(Department.id), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)
    salary = db.Column(db.Float)
    start_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Employee {self.id!r}>'
