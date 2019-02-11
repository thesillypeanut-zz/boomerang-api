from flask import request

from constants import EVENT_URL_PATH
from src.routes.decorators import json_response, token_required, json_request_validator
from src.services import event_service
from src.validation.event import create_validators, edit_validators


def add_routes(app):
    app.add_url_rule(
        rule=f'{EVENT_URL_PATH}/',
        methods=['GET'],
        view_func=list_events,
        endpoint=list_events.__name__
    ),
    app.add_url_rule(
        rule=f'{EVENT_URL_PATH}/',
        methods=['POST'],
        view_func=create_event,
        endpoint=create_event.__name__
    ),
    app.add_url_rule(
        rule=f'{EVENT_URL_PATH}/<user_id>',
        methods=['PUT'],
        view_func=edit_event,
        endpoint=edit_event.__name__
    ),
    app.add_url_rule(
        rule=f'{EVENT_URL_PATH}/<event_id>',
        methods=['GET'],
        view_func=get_event,
        endpoint=get_event.__name__
    ),
    app.add_url_rule(
        rule=f'{EVENT_URL_PATH}/<event_id>',
        methods=['DELETE'],
        view_func=delete_event,
        endpoint=delete_event.__name__
    )


@json_response(200)
@token_required
def list_events(current_user):
    return event_service.list_all({'organizer_id': current_user.id})


@json_response(200)
@token_required
def get_event(current_user, event_id):
    if not current_user.carts:
        return 'Unauthorized: You can only fetch your own carts.', 401

    if event_id not in [str(cart.id) for cart in current_user.carts]:
        return 'Unauthorized: You can only fetch your own carts.', 401

    return event_service.get(event_id)


@json_response(201)
@json_request_validator(create_validators.build)
def create_event():
    return event_service.create(request.json)


@json_response(200)
@json_request_validator(edit_validators.build)
@token_required
def edit_event(current_user, user_id):
    pass
    # return event_service.update(user_id, request.json)


@json_response(204)
@token_required
def delete_event(current_user, event_id):
    cart = event_service.get(event_id)

    if cart['customer_id'] != current_user.id:
        return 'Unauthorized: You can only delete your own carts.', 401

    return event_service.delete(event_id)
