import base64
import json
import unittest
from datetime import datetime

from constants import TEST_EVENT_URL_PATH
from tests.helpers import assert_error
from tests.unit.common import BaseTestCase


class EventTestCase(BaseTestCase):
    def test_create_event_is_successful(self):
        self.register_user()
        logged_in_user = self.login_user()
        token = json.loads(logged_in_user.get_data())['token']

        event_payload = {
            'name': 'Maliha\'s bday bash',
            'date': 'Mar 2 2019  7:00PM',
            'invitees': [
                {
                    'name': 'Maliha',
                    'phone': '+16478231710'
                },
                {
                    'phone': '+14155298990'
                }
            ],
            'sms_content': ''
        }

        response = self.client.post(
            f'{TEST_EVENT_URL_PATH}/',
            data=json.dumps(event_payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
