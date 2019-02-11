import jwt
from functools import wraps
from flask import make_response, jsonify, request

from instance.config import Config
from src.helpers import handle_exception
from src.services import event_service
from src.validation.models import User


def json_response(status_code):
    def outer_wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            payload = func(*args, **kwargs)

            if isinstance(payload, dict) or isinstance(payload, list):
                return make_response(jsonify(payload), status_code)
            return make_response(payload)

        return inner_wrapper

    return outer_wrapper


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return 'Unauthorized: Token is missing!', 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return 'Unauthorized: Token is invalid!', 401

        if not current_user:
            return 'Unauthorized: Token is invalid!', 401

        if request.url.split('/')[-1]:
            _validate_authorized_user(request.url, current_user)

        return f(current_user, *args, **kwargs)

    return decorated


def json_request_validator(build_validators):
    def outer_wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            validators = build_validators(request)
            for validator in validators:
                validator()  # raises an exception if a validation error occurs
            return func(*args, **kwargs)

        return inner_wrapper

    return outer_wrapper


def _validate_authorized_user(requested_url, current_user):
    resource = requested_url.split('/')[-2]
    resource_id = requested_url.split('/')[-1]

    if resource == 'users':
        if str(current_user.id) != resource_id:
            raise handle_exception('Unauthorized: You can only modify your own account.', 401)

    elif resource == 'events':
        if resource_id not in [str(event.id) for event in current_user.events]:
            raise handle_exception('Unauthorized: You can only fetch or modify your events.', 401)

        event = event_service.get(resource_id)
        if event['organizer_id'] != current_user.id:
            raise handle_exception('Unauthorized: You can only modify your events.', 401)