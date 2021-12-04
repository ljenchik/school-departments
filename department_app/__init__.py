from flask import Flask
from flask_migrate import Migrate

from .models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/dep'
db.init_app(app)
migrate = Migrate(app, db)

from .views import init_views
init_views()

from .rest import api