# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name

from datetime import datetime

from department_app.models.department import Department
from department_app.models.department_avg_salary import DepartmentAvgSalary

department_with_salaries_1 = DepartmentAvgSalary()
department_with_salaries_1.name = "Dep of Maths"
department_with_salaries_1.id = 1
department_with_salaries_1.avg_salary = 12345.68
department_with_salaries_1.date_created = datetime(2021, 12, 25)

department_with_salaries_2 = DepartmentAvgSalary()
department_with_salaries_2.name = "Dep of Phys"
department_with_salaries_2.id = 2
department_with_salaries_2.avg_salary = 897652.68
department_with_salaries_2.date_created = datetime(2020, 11, 1)

department_1 = Department()
department_1.name = "Dep of Maths Test"
department_1.id = 3
department_1.date_created = datetime(2021, 12, 26)
