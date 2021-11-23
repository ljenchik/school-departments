from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from werkzeug.exceptions import abort

from models.department import Department
from models.db_shared import db
from models.employee import Employee
from service.department_service import read_departments_with_salaries, create_department_or_error, get_department_by_id, \
    update_department

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/dep'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index_department():
    departments = read_departments_with_salaries()
    return render_template('departments.html', departments=departments)


@app.route('/add-department', methods=['POST', 'GET'])
def add_department():
    if request.method == 'POST':
        department_name = request.form['name']
        new_department = Department(name=department_name.strip())
        if new_department.name == '':
            return render_template('department.html', dep=new_department,
                                   error='Please, enter new department')
        error = create_department_or_error(new_department)
        if error is not None:
            return render_template('department.html', dep=new_department,
                               error=error)
        return redirect('/')
    else:
        new_department = Department(name='')
        return render_template('department.html', dep=new_department, error='')


def get_or_404(model):
    if model is None:
        abort(404)
    return model


@app.route('/edit-department/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    dep_to_edit = get_or_404(get_department_by_id(id))
    if request.method == 'POST':
        error = update_department(dep_to_edit, request.form['name'])
        if error is not None:
            return error
        return redirect('/')
    else:
        return render_template('department.html', dep=dep_to_edit)


@app.route('/delete-department/<int:id>')
def delete_department(id):
    dep_to_delete = get_or_404(get_department_by_id(id))
    try:
        db.session.delete(dep_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting this department'


@app.route('/department/<int:department_id>/employees')
def index_employee(department_id):
    employees = Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()
    dep = Department.query.get_or_404(department_id)
    return render_template('employees.html', employees=employees, department_name=dep.name,
                           department_id=department_id)


def validate_employee(emp: Employee) -> str:
    if relativedelta(emp.start_date, emp.date_of_birth).years < 18:
        return 'Employee must be at least 18 to start work'
    if datetime.today().year - emp.date_of_birth.year > 100:
        return "Please check employee's date of birth"


def parse_float(value):
    return float((value).replace(" ", "").replace(",", ""))


@app.route('/add-employee/<int:department_id>', methods=['POST', 'GET'])
def add_employee(department_id):
    if request.method == 'POST':
        dep = Department.query.get_or_404(department_id)
        new_employee = Employee(department_id=department_id)
        fill_employee_from_request(new_employee)
        validation_error = validate_employee(new_employee)

        if validation_error is not None:
            return render_template('employee.html', employee=new_employee, department_name=dep.name,
                                   department_id=department_id,
                                   error=validation_error)

        try:
            db.session.add(new_employee)
            db.session.commit()
            link = f'/department/{department_id}/employees'
            return redirect(link)
        except Exception as e:
            db.session.rollback()
            return render_template('employee.html', employee=new_employee, department_name=dep.name,
                                   department_id=department_id,
                                   error='There was an issue adding a new employee: ' + str(e))
    else:
        dep = Department.query.get_or_404(department_id)
        employee = Employee(name='', role='', salary='', start_date=datetime.today())
        return render_template('employee.html', employee=employee, department_name=dep.name, department_id=dep.id,
                               error='')


def fill_employee_from_request(new_employee):
    new_employee.name = request.form['name']
    new_employee.role = request.form['role']
    new_employee.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
    new_employee.salary = parse_float(request.form['salary'])
    new_employee.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')


@app.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    emp_to_edit = Employee.query.get_or_404(employee_id)
    dep = Department.query.get_or_404(emp_to_edit.department_id)

    if request.method == 'POST':
        fill_employee_from_request(emp_to_edit)
        validation_error = validate_employee(emp_to_edit)

        if validation_error is not None:
            return render_template('employee.html', employee=emp_to_edit, department_name=dep.name,
                                   department_id=dep.id, error=validation_error)

        try:
            db.session.commit()
            link = f'/department/{emp_to_edit.department_id}/employees'
            return redirect(link)
        except Exception as e:
            print('There was an issue adding a new employee: ' + str(e))
            db.session.rollback()
            return render_template('employee.html', employee=emp_to_edit, department_name=dep.name,
                                   department_id=dep.id,
                                   error='There was an issue editing an employee: ' + str(e))
    else:
        return render_template('employee.html', employee=emp_to_edit, department_name=dep.name, department_id=dep.id,
                               error='')


@app.route('/delete-employee/<int:employee_id>')
def delete_employee(employee_id):
    emp_to_delete = Employee.query.get_or_404(employee_id)
    try:
        db.session.delete(emp_to_delete)
        db.session.commit()
        link = f'/department/{emp_to_delete.department_id}/employees'
        return redirect(link)
    except:
        return 'There was an issue deleting this employee'


if __name__ == "__main__":
    app.run(debug=True)
