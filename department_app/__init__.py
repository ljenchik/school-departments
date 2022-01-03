"""
Imports Flask and Migrate, connects to database
"""
# pylint: disable=wrong-import-position, cyclic-import
from flask import Flask
from flask_migrate import Migrate

from config import Config
from .models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from .views import init_views

init_views()

from .rest import api
