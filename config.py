# pylint:disable=missing-module-docstring,missing-class-docstring
import os

from dotenv import load_dotenv

load_dotenv()

user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
server = os.environ.get('MYSQL_SERVER')
database = os.environ.get('MYSQL_DATABASE')
debug = os.environ.get('DEBUG')


class Config:
    # pylint: disable=too-few-public-methods
    DEBUG = debug
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{user}:{password}' \
                              f'@{server}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
