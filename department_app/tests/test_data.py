# pylint: skip-file

from datetime import datetime

from department_app.models.department import Department
from department_app.models.department_avg_salary import DepartmentAvgSalary
from department_app.models.employee import Employee

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

employee_1 = Employee()
employee_1.name = 'Anna Smith'
employee_1.role = 'Head of Department'
employee_1.date_of_birth = datetime(1985, 12, 5)
employee_1.salary = 33956
employee_1.start_date = datetime(2015, 9, 3)
employee_1.id = 1
employee_1.department_id = 1
employee_1.date_created = datetime(2020, 11, 1)

employee_2 = Employee()
employee_2.name = 'Alex Brown'
employee_2.role = 'Teacher'
employee_2.date_of_birth = datetime(1992, 2, 15)
employee_2.salary = 27453
employee_2.start_date = datetime(2015, 9, 3)
employee_2.id = 1
employee_2.department_id = 2
employee_2.date_created = datetime(2020, 11, 1)
