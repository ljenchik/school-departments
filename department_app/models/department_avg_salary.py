from department_app import db
from datetime import datetime


class DepartmentAvgSalary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    avg_salary = db.Column(db.Float)
    __tablename__ = 'Department_Avg_Salary_ignore'

    def __repr__(self):
        return '<Department_avg_salary %r>' % self.id
