from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/dep'
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Department %r>' % self.id


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
        departments = Department.query.order_by(Department.date_created).all()
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


@app.route('/department/<int:department_id>/employees', methods=['POST', 'GET'])
def index_emp(department_id):
    if request.method == 'POST':
        employee_name = request.form['name']
        new_employee = Employee(name=employee_name, department_id=department_id)
        try:
            db.session.add(new_employee)
            db.session.commit()
            link = f'/department/{department_id}/employees'
            return redirect(link)
        except:
            return 'There was an issue adding a new department'
    else:
        employees = Employee.query.filter_by(department_id=department_id).order_by(Employee.date_created).all()
        dep = Department.query.get_or_404(department_id)
        return render_template('employees.html', employees=employees, department_name=dep.name,
                               department_id=department_id)


@app.route('/add-employee/<int:id>')
def employee_add(id):
    dep = Department.query.get_or_404(id)
    return render_template('employee.html', employee=Employee(name='', role='', date_of_birth='', salary='', start_date=''),
                           department_name=dep.name, department_id = dep.id)


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


@app.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
def emp_edit(employee_id):
    emp_to_edit = Employee.query.get_or_404(employee_id)
    dep = Department.query.get_or_404(emp_to_edit.department_id)
    if request.method == 'POST':
        emp_to_edit.name = request.form['name']

        try:
            db.session.commit()
            link = f'/department/{emp_to_edit.department_id}/employees'
            return redirect(link)
        except:
            return 'There is an issue with editing this employee'
    else:
        return render_template('employee.html', employee=emp_to_edit, department_name=dep.name, department_id = dep.id)


if __name__ == "__main__":
    app.run(debug=True)
