from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('department.html', dep = Department(name = ''))


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


if __name__ == "__main__":
    app.run(debug=True)
