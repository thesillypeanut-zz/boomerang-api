from constants import MESSAGE_URL_PATH
from src.routes.decorators import json_response, token_required
from src.services import message_service


def add_routes(app):
    app.add_url_rule(
        rule=f'{MESSAGE_URL_PATH}/',
        methods=['GET'],
        view_func=list_messages,
        endpoint=list_messages.__name__
    ),
    app.add_url_rule(
        rule=f'{MESSAGE_URL_PATH}/<message_id>',
        methods=['GET'],
        view_func=get_message,
        endpoint=get_message.__name__
    ),


@json_response(200)
@token_required
def list_messages(current_user):
    return message_service.list_all()


@json_response(200)
@token_required
def get_message(current_user, message_id):
    return message_service.get(message_id)