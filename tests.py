"""
    This file tests features to see if they continue to work when new features
    are added. Everytime a new feature is added, a unittest should be written
    for it.
"""

import unittest
from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta


class UserModelCase(unittest.TestCase):
    # setUp + tearDown exec before+after each test
    def setUp(self):
        # use in-memory sqlite db for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all() # creates all tables from models into the db
    
    def tearDown(self):
        db.session.remove() # close then remove curr session
        db.drop_all() # drop all tables stored
    
    def test_password_hashing(self):
        u = User(username='jared_leto')
        u.set_password('HAHAHA')
        self.assertFalse(u.check_password('notfunny'))
        self.assertTrue(u.check_password('HAHAHA'))
    
    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=mp&s=128'))
    
    def test_follow(self):
        u1 = User(username='jack', email='jack@twitter.com')
        u2 = User(username='noah', email='noah@twitter.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        
        # confirm u1 is not following anyone nor followed
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])
        
        # jack followed noah
        u1.follow(u2)
        db.session.commit()
        
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'noah')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'jack')
            
    def test_follow_posts(self):
        u1 = User(username='jack', email='jack@twitter.com')
        u2 = User(username='noah', email='noah@twitter.com')
        u3 = User(username='biz', email='biz@twitter.com')
        u4 = User(username='evan', email='evan@twitter.com')
        
        # add four users to db
        db.session.add_all([u1, u2, u3, u4]) 
        
        # create post for each user with staggered times
        now = datetime.utcnow()
        p1 = Post(body='jacks post', author=u1,
                  timestamp=now+timedelta(seconds=1)) # add 1 sec to now
        p2 = Post(body='noahs post', author=u2,
                  timestamp=now+timedelta(seconds=4))  # add 4 sec to now
        p3 = Post(body='bizs post', author=u3,
                  timestamp=now+timedelta(seconds=3)) 
        p4 = Post(body='evanss post', author=u4,
                  timestamp=now+timedelta(seconds=2))
        # add four posts to db
        db.session.add_all([p1, p2, p3, p4])
        # commit changes
        db.session.commit()
        
        # setup followers
        u1.follow(u2) # jack follows noah
        u1.follow(u4) # jack follows evan
        u2.follow(u3) # noah follows biz
        u3.follow(u4) # biz follows evan
        db.session.commit()
        
        # check followed posts for each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)