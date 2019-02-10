import base64
import json
import unittest

from constants import TEST_USER_URL_PATH
from tests.helpers import assert_error
from tests.unit.common import BaseTestCase


class EventTestCase(BaseTestCase):
    def test_create_event_is_successful(self):
        user_payload = {
            'first_name': 'Maliha',
            'last_name': 'Islam',
            'email': 'maliha@abc.com',
            'password': 'PASSWORD'
        }

        response = self.client.post(
            f'{TEST_USER_URL_PATH}/',
            data=json.dumps(user_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        valid_credentials = base64.b64encode(b'maliha@abc.com:PASSWORD').decode('utf-8')
        response = self.client.get(
            f'{TEST_USER_URL_PATH}/login',
            headers={'Authorization': f'Basic {valid_credentials}'}
        )
        assert 'token' in json.loads(response.get_data())


    def test_create_user_with_invalid_or_missing_field_raises_error(self):
        user_payload_with_missing_field = {
            'first_name': 'Maliha',
            'last_name': 'Islam',
            'email': 'maliha@def.com'
        }

        response = self.client.post(
            f'{TEST_USER_URL_PATH}/',
            data=json.dumps(user_payload_with_missing_field),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert_error(
            response.data,
            'Bad Request: One or more required fields are missing or invalid: first_name, last_name, email, password'
        )

        user_payload_with_invalid_field = {
            'first_name': 'Maliha',
            'last_name': 'Islam',
            'email': 'maliha@abc.com',
            'password': 'PASSWORD',
            'INVALID': 'invalid'
        }

        response = self.client.post(
            f'{TEST_USER_URL_PATH}/',
            data=json.dumps(user_payload_with_invalid_field),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        assert_error(
            response.data,
            'Bad Request: One or more required fields are missing or invalid: first_name, last_name, email, password'
        )


    def test_list_all_users_is_successful(self):
        self.register_user()
        self.register_user('user2@test.com')
        self.register_user('user3@test.com')

        logged_in_user = self.login_user()
        token = json.loads(logged_in_user.get_data())['token']

        response = self.client.get(
            f'{TEST_USER_URL_PATH}/',
            headers={'x-access-token': token}
        )
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)


    def test_get_user_is_successful(self):
        user = self.register_user()
        user_id = json.loads(user.get_data())['id']
        logged_in_user = self.login_user()
        token = json.loads(logged_in_user.get_data())['token']

        response = self.client.get(
            f'{TEST_USER_URL_PATH}/{user_id}',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 200)


    def test_update_user_is_successful(self):
        user = self.register_user()
        user_id = json.loads(user.get_data())['id']
        logged_in_user = self.login_user()
        token = json.loads(logged_in_user.get_data())['token']

        response = self.client.get(
            f'{TEST_USER_URL_PATH}/{user_id}',
            headers={'x-access-token': token}
        )
        assert json.loads(response.get_data())['first_name'] == 'John'

        updated_user = {
            'first_name': 'Maliha'
        }
        response = self.client.put(
            f'{TEST_USER_URL_PATH}/{user_id}',
            data=json.dumps(updated_user),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.get_data())['first_name'] == 'Maliha'


    def test_update_user_with_invalid_field_raises_error(self):
        user = self.register_user()
        user_id = json.loads(user.get_data())['id']
        logged_in_user = self.login_user()
        token = json.loads(logged_in_user.get_data())['token']

        updated_user = {
            'INVALID': 'invalid'
        }
        response = self.client.put(
            f'{TEST_USER_URL_PATH}/{user_id}',
            data=json.dumps(updated_user),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 400)
        assert_error(
            response.data,
            'Bad Request: Field "INVALID" is not allowed. Allowed fields are: first_name, last_name, password'
        )


    def test_update_user_with_unauthorized_user_login_raises_error(self):
        self.register_user()
        logged_in_user = self.login_user()
        token = json.loads(logged_in_user.get_data())['token']

        user2 = self.register_user('user2@test.com')
        user2_id = json.loads(user2.get_data())['id']

        updated_user = {
            'first_name': 'Maliha'
        }
        response = self.client.put(
            f'{TEST_USER_URL_PATH}/{user2_id}',
            data=json.dumps(updated_user),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 401)
        assert_error(
            response.data,
            'Unauthorized: You can only modify your own account.'
        )


    def test_delete_user_is_successful(self):
        user = self.register_user()
        user_id = json.loads(user.get_data())['id']
        logged_in_user = self.login_user()
        token = json.loads(logged_in_user.get_data())['token']

        response = self.client.delete(
            f'{TEST_USER_URL_PATH}/{user_id}',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 204)


    def test_delete_user_without_token_raises_error(self):
        user = self.register_user()
        user_id = json.loads(user.get_data())['id']

        response = self.client.delete(
            f'{TEST_USER_URL_PATH}/{user_id}',
        )
        self.assertEqual(response.status_code, 401)
        assert_error(
            response.data,
            'Unauthorized: Token is missing!'
        )


if __name__ == "__main__":
    unittest.main()
