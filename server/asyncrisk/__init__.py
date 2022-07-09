import logging

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from . import env


app_env = env.detect_environment()

# configure some details of the flask app object
app = Flask(__name__)
app.config['DEBUG'] = app_env.debug
app.config['SQLALCHEMY_DATABASE_URI'] = app_env.database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = app_env.secret_key

bootstrap = Bootstrap(app)

# setup login/auth configuration
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# setup logging
logFormatStr = '%(levelname)s %(asctime)-8s %(message)s'
formatter = logging.Formatter(fmt=logFormatStr, datefmt='%Y-%m-%d %H:%M:%S')

fileHandler = RotatingFileHandler(app_env.logs_filename, maxBytes=100000, backupCount=1)
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.DEBUG)
app.logger.addHandler(fileHandler)

from asyncrisk import routes
