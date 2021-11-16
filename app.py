from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/dep'
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Department %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        department_name = request.form['name']
        new_department = Department(name = department_name)

        try:
            db.session.add(new_department)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding a new department'
    else:
        return render_template('departments.html')

@app.route('/edit-dep')
def departmet_add():
    return render_template('department.html')


if __name__ == "__main__":
    app.run(debug=True)