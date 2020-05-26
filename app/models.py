from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# User table in db
class User(UserMixin, db.Model):
	# everytime this changes, db migration is need (flask db migrate -m '')
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	# Post refers to 'many' side of this 1tomany relationship
	# backref : post.author returns author of post
	# lazy : how db query fo rleationship will be issued
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(20))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f'<User {self.username}>'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return f'https://www.gravatar.com/avatar/{digest}?d=mp&s={size}'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(70))
	# for default, passing function not return value. (thats why no ())
	# also by default use UTC and convert upon displaying to user localtime
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# user.id refers to class(User) but sqlalchemy only recongizes lowercase
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f'<Post {self.body}>'

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

