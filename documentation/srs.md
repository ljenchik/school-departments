### Software Requirement Specification

### Departments

Departments is web-application which allows users to record information about departments and employees. Application
provides:

    • Displays a list of departments
    • Updates the list of departments (adding, editing, deleting)
    • Displays a list of department employees
    • Updates the list of employees (adding, editing, deleting)
    • Searches employee by his/her exact date of birth
    • Searches employees with their birth dates between two given dates 

**1. Departments**

The mode is designed to view a list of departments. Users see the list of existing departments (example is about
departments of Brentwood Ursuline Convent High School for girls) with average salary for each department. Average salary
is displayed only if department employees' list is not empty.

**Departments**

of Brentwood Ursuline Convent High School for girls

[Departments]() &nbsp; [Search]()

| Name | Avg Salary | | |
| ---  | ---- | ---| --- |
| Department of Mathematicss | 32093.23 | [Edit]() | [Delete]() |
| Department of Modern Foreign Languages | 30093.0 | [Edit]() | [Delete]() |
| Department of Art | 29045.23 | [Edit]() | [Delete]() |

[Add department]()

"Departments" link at the header leads to the main page which displays a list of all departments.

"Search" link allows to search employees by their birth dates

**1.1 Add department**

**Main scenario**

    • User clicks the “Add department” button in the departments list view mode
    • Application displays form to enter department name
    • User enters department name and presses “Save” button
    • If department name is entered incorrectly, for example, as empty or duplicate department name, corresponding incorrect data messages will be displayed displayed
    • If entered department name is valid, then record is adding to database
    • If error occurs, then error message will be displayed
    • If new department record is successfully added, then list of departments with added record will be displayed
    • User should click on “Back to departments” link in order to go to list of departments

**Cancel operation scenario**

    • User clicks “Add department” button in the departments list view mode 
    • Application displays a form to enter department name 
    • User enters department name or leaves the form empty, then presses “Cancel” button
    • Data don’t save in data base, then list of departments is displaying to user

**1.2 Edit department**

**Main scenario**

    • User clicks “Edit” button in the departments list view mode
    • Application displays a form to enter department name
    • User enters department name and presses “Save” button
    • If department name is entered incorrectly, for example, as empty or duplicate department name, corresponding incorrect data messages are displayed
    • If entered department name is valid, then record is adding to database
    • If error occurs, then error message will be displayed
    • If new department record is successfully added, then list of departments with updated record will be displayed

**Cancel operation scenario**

    • User clicks “Edit” button in the departments list view mode 
    • Application displays a form to enter department name 
    • User changes department name or leaves the form empty, then presses “Cancel” button
    • Data don’t save in database, then the list of departments will be displayed

**Employees**

The mode is intended for viewing and editing employees of a chosen department.

**Main scenario**

    • User selects one department from the list of existing departments
    • Application displays a list of employees of this department

The list displays the following columns:

    • Name – employee’s surname and name
    • Role employee’s position within department
    • Date of birth – employee’s date of birth
    • Salary – employee’s salary in £
    • Start date – employee’s first date at work

**Employees**

Department of Mathematics

[Departments]() &nbsp; [Search]()

| Name  |  Role | Date of birth  |  Salary  | Start Date | | |
|---|---|---|---|---|---|---|
| Alex White | Head of Department | 13/07/1983 | 45780.59 | 03/09/2015 | [Edit]() | [Delete]() |
| Anna Black | Teacher | 4/6/1987 | 35780.59 | 03/09/2020 | [Edit]() | [Delete]() |

[Add employee]()

**2.1 Add employee**

    • User clicks “Add employee” button in employees list view mode 
    • Application displays forms to enter employee’s name, role, date of birth, salary, start date
    • User enters data and presses “Save” button
    • If one of the forms is entered incorrectly or left empty, corresponding incorrect data messages are displayed
    • If entered employee’s data are valid, then record is adding to database
    • If error occurs, then error message will be displayes

Constraints for data validation:

    • Name – maximum length of 200 characters
    • Role – maximum length of 100 characters
    • Date of birth – should be no less than 100 years from the current date
    • Date of birth and Start date – in format dd/mm/yyyy
    • Start date – employee should be at least 18 years old 

**Employees**

Department of Mathematics

[Departments]() &nbsp; [Search]()

---
Employee's name

---
Employee's role

---
Employee's date of birth

---

Employee's salary

---
Employee's start date

---
[Save]() &nbsp; [Cancel]()

**Cancel operation scenario**

    • User clicks “Add employee” button in the employees list view mode 
    • Application displays forms to enter employee’s name, role, date of birth, salary, start date
    • User enters employee’s data or leaves form/forms empty, then presses “Cancel” button
    • Data don’t save in data base, then list of employees will be displayed

**1.2 Edit employee**

**Main scenario**

    • User clicks “Edit” button in the employees list view mode
    • Application displays forms to enter employee’s name, role, date of birth, salary, start date
    • User enters employee’s new data and presses “Save” button
    • If one of the forms is entered incorrectly or left empty, corresponding incorrect data messages are displayed
    • If entered employee’s data are valid, then record is adding to database
    • If error occurs, then error message will be displayed
    • If new employee record is successfully added, then list of employees with updated record will be displayed

**Employees**

Department of Mathematics

[Departments]() &nbsp; [Search]()

---
Employee's name

Ben Brown

---
Employee's role

Teacher

---
Employee's date of birth

25/08/1984

---

Employee's salary

34567.26

---
Employee's start date

02/09/2020

---
[Save]() &nbsp; [Cancel]()

**Cancel operation scenario**

    • User clicks “Edit” button in the employees list view mode 
    • Application displays forms of existing employee's name, role, date of birth, salary, start date
    • User changes employee’s data or leaves the form/forms empty, then presses “Cancel” button
    • Data don’t save in data base, then list of employees will be displayed

**3. Search**

The mode is designed to search employees by their birthdays as well as when their birthdays are between two given dates.
The list of employees, with departments names where employees belong to, will be displayed.

**Main scenario**

    • User clicks “Search” button at the header of any page
    • Application displays forms to enter date of birth or two dates: from and to
    • A) User enters exact employee’s date of birth and presses “Search” button
    • B) or user enters two dates and presses “Search” button
    • If employees with required date of birth exist or their birthdays are between two given dates, then they will be displayed with their corresponding departments
    • If user clicks on department name link (cecond column), the list of all employees of the chosen department will be displayed

**Search**

by date of birth

[Departments]() &nbsp; [Search]()

|Date of birth|  dd/mm/yyyy |   [Search]()
|---|---|----|

|From| dd/mm/yyyy| To| dd/mm/yyyy | [Search]()
|---|---|----|---|---|

**Scenario A)**

**Search**

by date of birth

[Departments]() &nbsp; [Search]()

|Date of birth| 13/07/1983 |   [Search]()
|---|---|----|

|From| dd/mm/yyyy| To| dd/mm/yyyy | [Search]()
|---|---|----|---|---|

| Employee Name  | Department | Role | Date of birth  |  Salary  | Start Date | | |
|---|---|---|---|---|---|---|---|
| Alex White | [Department of Mathematics]() |Head of Department | 13/07/1983 | 45780.59 | 03/09/2015 | [Edit]() | [Delete]() |

**Scenario B)**
**Search**

by date of birth

[Departments]() &nbsp; [Search]()

|Date of birth| dd/mm/yyyy |   [Search]()
|---|---|----|

|From| 12/12/1986| To| 01/01/1998 | [Search]()
|---|---|----|---|---|

| Employee Name  | Department | Role | Date of birth  |  Salary  | Start Date |
|---|---|---|---|---|---|
| Sue Fox | [Department of Arts]() |Teacher | 13/07/1991 | 25780.59 | 03/09/2015 |
| Angela Harris | [Department of Science]() |Teacher | 12/12/1987 | 35767.59 | 02/09/2020 |

