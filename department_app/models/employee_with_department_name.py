from datetime import datetime

from department_app import db


class EmployeeDepName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    role = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)
    salary = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    department_id = db.Column(db.Integer, nullable=False)
    department_name = db.Column(db.Integer, nullable=False)
    __tablename__ = 'Employee_with_department_name_ignore'

    def __repr__(self):
        return f'<Employee_with_department_name {id}>'
