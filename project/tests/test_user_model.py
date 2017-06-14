# project/tests/test_user_model.py


from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('test@test.com', 'test@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test@test.com')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    def test_add_user_duplicate_username(self):
        add_user('test@test.com', 'test@test.com', 'test')
        duplicate_user = User(
            username='test@test.com',
            email='test@test2.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('test@test.com', 'test@test.com', 'test')
        duplicate_user = User(
            username='test@test2.com',
            email='test@test.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('test@test.com', 'test@test.com', 'test')
        user_two = add_user('test@test2.com', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)
