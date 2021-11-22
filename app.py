from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/dep'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = {'info': dict(is_view=True)}


    def __repr__(self):
        return '<Department %r>' % self.id

class Department_Avg_Salary(Department):
    avg_salary = db.Column(db.Float)

    def __repr__(self):
        return '<Department_avg_salary %r>' % self.id


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, ForeignKey(Department.id), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)
    salary = db.Column(db.Float)
    start_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Employee %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        department_name = request.form['name']
        new_department = Department(name=department_name)
        try:
            db.session.add(new_department)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding a new department'
    else:
        departments = Department_Avg_Salary.query.from_statement(
            db.text("""select d.*, avg_salary
                    from department d 
                    join (
                        select d.id, round(avg(e.salary), 2) avg_salary
                        from department d 
                        join employee e on d.id  = e.department_id 
                        GROUP by d.id
                    ) avg_sal on avg_sal.id = d.id
                    """)
        ).all()
        return render_template('departments.html', departments=departments)


@app.route('/add-dep')
def departmet_add():
    return render_template('department.html', dep=Department(name=''))


@app.route('/delete/<int:id>')
def delete(id):
    dep_to_delete = Department.query.get_or_404(id)
    try:
        db.session.delete(dep_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting this department'


@app.route('/edit-dep/<int:id>', methods=['GET', 'POST'])
def edit(id):
    dep_to_edit = Department.query.get_or_404(id)
    if request.method == 'POST':
        dep_to_edit.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There is an issue with editing this department'
    else:
        return render_template('department.html', dep=dep_to_edit)


@app.route('/department/<int:department_id>/employees')
def index_emp(department_id):
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
def employee_add(department_id):
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
            print('There was an issue adding a new employee: ' + str(e))
            db.session.rollback()
            return render_template('employee.html', employee=new_employee, department_name=dep.name,
                                   department_id=department_id,
                                   error='There was an issue adding a new employee: ' + str(e))
    else:
        dep = Department.query.get_or_404(department_id)
        employee = Employee(name='', role='', salary='', start_date=datetime.today())
        return render_template('employee.html', employee=employee, department_name=dep.name, department_id=dep.id, error='')


def fill_employee_from_request(new_employee):
    new_employee.name = request.form['name']
    new_employee.role = request.form['role']
    new_employee.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
    new_employee.salary = parse_float(request.form['salary'])
    new_employee.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')




@app.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
def emp_edit(employee_id):
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
def emp_delete(employee_id):
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
