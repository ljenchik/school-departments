"""
This package contains department and employee models:
Modules:
- `department.py`: represents departments
- `department_avg_salary.py`: represents departments with average salaries
- `employee.py`: defines employees model
- 'employee_with_department_name.py' : defines employee with department name model, used in search
"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
