"""
Imports Flask and Migrate, connects to database
"""
# pylint: disable=wrong-import-position, cyclic-import
import logging.config
import sys

from flask import Flask
from flask_migrate import Migrate
from config import Config
from .models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
# logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

file_handler = logging.FileHandler(filename='app.log', mode='w')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

# pylint: disable=no-member
logger = app.logger
logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers.clear()
werkzeug_logger.addHandler(file_handler)
werkzeug_logger.addHandler(console_handler)
werkzeug_logger.setLevel(logging.DEBUG)

# sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
# sqlalchemy_logger.addHandler(file_handler)
# sqlalchemy_logger.addHandler(console_handler)
# sqlalchemy_logger.setLevel(logging.DEBUG)

from .views import init_views

init_views()

from .rest import api
