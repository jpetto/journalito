#!/usr/bin/env python
import unittest

from app import create_app, db
from app.models import Post, User
from config import Config


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = '123456passwordadmin111111'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        # the following two lines are handled automatically by flask i guess?
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='Dougie')
        u.set_password('teachmehowto')
        self.assertFalse(u.check_password('fresh'))
        self.assertTrue(u.check_password('teachmehowto'))

    def test_password_reset_token(self):
        u = User(username='violet', email='violet@testing.com')
        u.set_password('forcebubbles!')
        db.session.add(u)
        db.session.commit()
        token = u.get_reset_password_token()
        check_user = User.verify_reset_password_token(token)
        self.assertEqual(u.id, check_user.id)


if __name__ == '__main__':
    unittest.main(verbosity=2)
