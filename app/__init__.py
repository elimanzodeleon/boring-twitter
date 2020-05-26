from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config) # apply config to app
db = SQLAlchemy(app) # db obj to repr db
migrate = Migrate(app, db) # obj to repr migration engine
login = LoginManager(app)
# some pages require to be logged in to view, this is where user will be redirected when propmted to sign in to view page
login.login_view = 'login'

# import below to avoid circular import
from app import routes, models
