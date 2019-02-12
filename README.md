# Boomerang API (in Progress)

A server side web API that uses CRUD operations to create events, send bulk SMS invites and view invitee responses, 
built using the Flask microframework, SQLite database and [Twilio Programmable SMS API](https://www.twilio.com/docs/sms). 

## Requirements

On a Linux environment, run the following commands:
```bash
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python3.6-dev
sudo apt-get update
sudo apt-get install curl
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

## Getting Started

```bash
# Clone this repository and cd into it:
git clone https://github.com/thesillypeanut/boomerang-api.git
cd boomerang-api/

# Create and activate your virtual environment:
virtualenv venv
source venv/bin/activate

# Install your project dependencies:
pip install -r requirements.txt

# Start the server:
python3 run.py
```

## Database Models
The design of this database model was inspired by 
[Database Model for a Messaging System](https://www.vertabelo.com/blog/technical-articles/database-model-for-a-messaging-system).
<img src="/database_design.png">

## Try Out the API

This is a sample testing flow of creating an event, inviting guests and viewing invitee responses.

Create a user:
```bash
curl -H "Content-Type: application/json" -X POST -d <USER_PAYLOAD> https://boomerang-flask-react.herokuapp.com/api/v1/users/

# Sample user payload:
'{
    "email": "maliha@abc.com",
    "password": "PASSWORD",
    "first_name": "Maliha",
    "last_name": "Islam"
}'
```

Login the user:
```bash
curl --user <EMAIL>:<PASSWORD> https://boomerang-flask-react.herokuapp.com/api/v1/users/login
```
You will receive an authentication token. Please note that you need to use the token you received in the previous step 
to perform most requests from here on. For your convenience, you can save the token in an environment variable:
```bash
export TOKEN="YOUR-TOKEN-HERE"
echo "$TOKEN"
```
Your token will expire in 1 hour. Login again to get a new token and update your environment variable as necessary.

Create an event:
```bash
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X POST -d <EVENT_PAYLOAD> https://boomerang-flask-react.herokuapp.com/api/v1/events/

# Sample event payload:
'{
    "name": "Malihas bday bash",
    "date": "Mar 2 2019  7:00PM",
    "invitees": [
        {
            "name": "Sam",
            "phone": "+14161231111"
        },
        {
            "name": "Monica",
            "phone": "+14161230000"
        }
    ],
    "sms_content": "Bring me some cupcakes :P"
}'
```
Note that this API uses a Twilio trial account. As a result, one of the limitations is that the phone numbers you send
sms messages to must be verified by me. Email me at ism.maliha@gmail.com if you need to verify a number.

Fetches all messages:
```bash
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X GET https://boomerang-flask-react.herokuapp.com/api/v1/messages/
```

To track responses to invites, specifically one of the event invitees:
1. Fetch an event invitee -> get message recipient id
2. Fetch a message recipient by message recipient id -> get message_id
3. Query messages using parent_message_id=message_id -> this is the response from the event invitee


## Migrations
Migrations need to be run to propagate changes we make to our models (eg. adding a field, deleting a model).
Flask-Migrate uses Alembic to autogenerate migrations for us.

```bash
# Initialize migrations:
python3 manage.py db init

# Run migrations:
python3 manage.py db migrate

# Apply migrations to the database:
python3 manage.py db upgrade
```

## Testing
Unit tests are written to automate testing for the various services.

```bash
# Run all tests:
pytest

# Run all tests with debugging (no capture):
pytest -s

# Run a single test (file-path::class-name::test-name):
pytest tests/unit/test_user_service.py::UserTestCase::test_list_all_users_is_successful
```