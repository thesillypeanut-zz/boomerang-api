import base64
import json
from unittest import TestCase

from constants import TEST_USER_URL_PATH
from src import create_app, db


class BaseTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.client.testing = True

        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def register_user(self, email='user@test.com', password='test1234'):
        user_data = {
            'email': email,
            'password': password,
            'first_name': 'John',
            'last_name': 'Doe'
        }
        return self.client.post(
            f'{TEST_USER_URL_PATH}/',
            data=json.dumps(user_data),
            content_type='application/json'
        )


    def login_user(self, email='user@test.com', password='test1234'):
        valid_credentials = base64.b64encode(f'{email}:{password}'.encode('utf-8')).decode('utf-8')
        return self.client.get(
            f'{TEST_USER_URL_PATH}/login',
            headers={'Authorization': f'Basic {valid_credentials}'}
        )
