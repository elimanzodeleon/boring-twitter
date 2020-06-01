import os
import logging
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

app.config.from_object(Config) # apply config to app
db = SQLAlchemy(app) # db obj to repr db
migrate = Migrate(app, db) # obj to repr migration engine
login = LoginManager(app)
# some pages require to be logged in to view, this is where user will be redirected when propmted to sign in to view page
login.login_view = 'login'

# import below to avoid circular import
from app import routes, models, errors

# error logging
if not app.debug:
	# check if logs dir exists. if not, make one
	if not os.path.exists('logs'):
		os.makedirs('logs')
	# create log file
	file_handler = RotatingFileHandler('logs/boring_twitter.log',
										maxBytes=10240,
										backupCount=10)

	file_handler.setFormatter(logging.Formatter(
	'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('boring twitter')

