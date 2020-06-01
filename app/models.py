from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# association table (AT) for follower/followed
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey(
                         'user.id')),  # id of user who is following
                     db.Column('followed_id', db.Integer, db.ForeignKey(
                         'user.id'))  # id of user who is being followed
                     )


# User table in db
class User(UserMixin, db.Model):
    # everytime this changes, db migration is need (flask db migrate -m '')
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Post refers to 'many' side of this 1tomany relationship
    # backref : post.author returns author of post
    # lazy : query dn run until until it is specifically requested
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(20))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # User: left side fo table (right side is parent which is also User)
    # secondary: configures assoc. table used for this relationship
    # primary: cond where left entity(follower) is linked with AT
    # secondary: cond where right entity(followed) is linked with AT
    # backref: how right side entity(followed) is accessed
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
                               )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=mp&s={size}'

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    # .filter allows arbitrary filtering conditions. .filter_by only constants
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == \
                                    user.id).count() > 0
    
    # get posts of followed users
    def followed_posts(self):
        # join: join posts+followers where RS followed_id = Post.user_id
        # filter: where followers follower_id = curr user id (self.id)
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
    
        # merge own posts with posts from those followed in descending order
        return followed.union(own).order_by(Post.timestamp.desc())
    


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
