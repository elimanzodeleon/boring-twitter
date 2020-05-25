from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config) # apply config to app
db = SQLAlchemy(app) # db obj to repr db
migrate = Migrate(app, db) # obj to repr migration engine

# import below to avoid circular import
from app import routes, models
