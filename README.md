# Departments App

## This app:

- ### Displays a list of departments and the average salary of these departments

- ### Displays a list of employees of each department

- ### Searches employees born on a specific date or in the period between two given dates

- ### Adds, edits, deletes departments and employees

## To build a project you need:

- ### Navigate to the root folder

- ### Optionally set up and activate the virtual environment:

```
virtualenv venv
source env/bin/activate
```

- ### Install the requirements:

```
pip install -r requirements.txt
```

- ### Set the following environment variables:

```
MYSQL_USER=<your_mysql_user>
MYSQL_PASSWORD=<your_mysql_user_password>
MYSQL_SERVER=<your_mysql_server>
MYSQL_DATABASE=<your_mysql_database_name>
```

- ### Run migrations to create database tables:

```
flask db upgrade
```

- ### Run web app

```
python -m flask run
```

or

```
gunicorn -w 4 app:app
```

## You can access the web service and web application on the following addresses:

- ### Rest Api:

```
localhost:5000/api/departments

localhost:5000/api/departments/<int:department_id>
localhost:5000/api/employee/<int:employee_id>
localhost:5000/api/department/<int:department_id>/employee

localhost:5000/api/employee/search
localhost:5000/api/employee/search?date_of_birth=<YYYY-MM-DD>
localhost:5000/api/employee/search?date_from=<YYYY-MM-DD>&date_to=<YYYY-MM-DD>
```

#### Web Service endpoints are documented with SwaggerUI at:

```
localhost:5000/swagger
```

- ### Web Application:

```
localhost:5000/

localhost:5000/department/add
localhost:5000/department/edit/<int:department_id>
localhost:5000/department/<int:department_id>/employees

localhost:5000/add-employee/<int:department_id>
localhost:5000/edit-employee/<int:employee_id>
localhost:5000/search-employee
```