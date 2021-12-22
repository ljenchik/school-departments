"""
This package contains modules defining department and employee models:
Modules:
- `department.py`: defines model representing departments
- `department_avg_salary.py`: defines model representing departments with average salaries
- `employee.py`: defines model representing employees
- 'employee_with_department_name.py' : defines model representing employee
with department name used in search
"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
