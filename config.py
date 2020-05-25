# file containing configuration data (secret key, etc)

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	# secretkey used in conjunction with form.hidden_tag()
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'krusty_krab_secret_formula'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
