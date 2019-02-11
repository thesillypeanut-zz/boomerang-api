_LOCAL_HOST_URL_PATH = 'http://127.0.0.1:5000'
_HEROKU_URL_PATH = 'https://boomerang-flask-react.herokuapp.com'
_BASE_URL_PATH = '/api/v1'

# routes
USER_URL_PATH = f'{_BASE_URL_PATH}/users'
DB_URL_PATH = f'{_BASE_URL_PATH}/db'
EVENT_URL_PATH = f'{_BASE_URL_PATH}/events'
TWILIO_URL_PATH = f'{_BASE_URL_PATH}/twilio'

TWILIO_CALLBACK_PATH = f'{_HEROKU_URL_PATH}{_BASE_URL_PATH}/twilio/delivery'

# test routes
TEST_USER_URL_PATH = f'{_HEROKU_URL_PATH}{_BASE_URL_PATH}/users'
TEST_EVENT_URL_PATH = f'{_HEROKU_URL_PATH}{_BASE_URL_PATH}/events'
