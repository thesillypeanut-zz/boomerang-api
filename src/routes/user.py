from flask import request

from constants import USER_URL_PATH
from src.routes.decorators import json_response, token_required, json_request_validator
from src.services import user_service
from src.validation.user import edit_validators, create_validators


def add_routes(app):
    app.add_url_rule(
        rule=f'{USER_URL_PATH}/',
        methods=['GET'],
        view_func=list_users,
        endpoint=list_users.__name__
    ),
    app.add_url_rule(
        rule=f'{USER_URL_PATH}/<user_id>',
        methods=['GET'],
        view_func=get_user,
        endpoint=get_user.__name__
    ),
    app.add_url_rule(
        rule=f'{USER_URL_PATH}/',
        methods=['POST'],
        view_func=create_user,
        endpoint=create_user.__name__
    ),
    app.add_url_rule(
        rule=f'{USER_URL_PATH}/<user_id>',
        methods=['PUT'],
        view_func=edit_user,
        endpoint=edit_user.__name__
    ),
    app.add_url_rule(
        rule=f'{USER_URL_PATH}/<user_id>',
        methods=['DELETE'],
        view_func=delete_user,
        endpoint=delete_user.__name__
    ),
    app.add_url_rule(
        rule=f'{USER_URL_PATH}/login',
        methods=['GET'],
        view_func=login_user,
        endpoint=login_user.__name__
    )


# TODO: only allow admins to access this route
@json_response(200)
@token_required
def list_users(current_user):
    return user_service.list_all(request.args)


# TODO: only allow admins to access this route
@json_response(200)
@token_required
def get_user(current_user, user_id):
    return user_service.get(user_id)


@json_response(201)
@json_request_validator(create_validators.build)
def create_user():
    return user_service.create(request.json)


@json_response(200)
@json_request_validator(edit_validators.build)
@token_required
def edit_user(current_user, user_id):
    return user_service.update(user_id, request.json)


@json_response(204)
@token_required
def delete_user(current_user, user_id):
    return user_service.delete(user_id)


@json_response(200)
def login_user():
    return user_service.login(request.authorization)
