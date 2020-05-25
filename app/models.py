from app import db
from datetime import datetime

# User table in db
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	# Post refers to 'many' side of this 1tomany relationship
	# backref : post.author returns author of post
	# lazy : how db query fo rleationship will be issued
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return f'<User {self.username}>'

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
