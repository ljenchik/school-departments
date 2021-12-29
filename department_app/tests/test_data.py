# pylint: skip-file

from datetime import datetime

from department_app.models.department import Department
from department_app.models.department_avg_salary import DepartmentAvgSalary
from department_app.models.employee import Employee
from department_app.models.employee_with_department_name import EmployeeDepName

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
employee_1.salary = 33956.5
employee_1.start_date = datetime(2015, 9, 3)
employee_1.id = 1
employee_1.department_id = 1
employee_1.date_created = datetime(2020, 11, 1)

employee_2 = Employee()
employee_2.name = 'Alex Brown'
employee_2.role = 'Teacher'
employee_2.date_of_birth = datetime(1992, 2, 15)
employee_2.salary = 27453.0
employee_2.start_date = datetime(2015, 9, 3)
employee_2.id = 2
employee_2.department_id = 2
employee_2.date_created = datetime(2020, 11, 1)

employee_3 = EmployeeDepName()
employee_3.name = 'Roy Hilton'
employee_3.role = 'Head of Department'
employee_3.date_of_birth = datetime(1975, 4, 25)
employee_3.salary = 43956.0
employee_3.start_date = datetime(2000, 9, 10)
employee_3.id = 3
employee_3.department_id = 3
employee_3.date_created = datetime(2020, 12, 29)

employee_4 = Employee()
employee_4.name = 'Bob Marley'
employee_4.role = 'Teacher'
employee_4.date_of_birth = datetime(1982, 12, 4)
employee_4.salary = 37453.0
employee_4.start_date = datetime(2012, 9, 3)
employee_4.id = 4
employee_4.department_id = 2
employee_4.date_created = datetime(2021, 11, 10)

employee_5 = EmployeeDepName()
employee_5.name = 'Natalie Ashford'
employee_5.role = 'Teacher'
employee_5.date_of_birth = datetime(1975, 1, 1)
employee_5.salary = 28956.34
employee_5.start_date = datetime(2003, 9, 3)
employee_5.id = 5
employee_5.department_id = 4
employee_5.department_name = 'Department of Arts'
employee_5.date_created = datetime(2021, 11, 10)
