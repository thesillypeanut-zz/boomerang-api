from constants import MESSAGE_RECIPIENT_URL_PATH
from src.routes.decorators import json_response, token_required
from src.services import message_recipient_service


def add_routes(app):
    app.add_url_rule(
        rule=f'{MESSAGE_RECIPIENT_URL_PATH}/',
        methods=['GET'],
        view_func=list_message_recipients,
        endpoint=list_message_recipients.__name__
    ),
    app.add_url_rule(
        rule=f'{MESSAGE_RECIPIENT_URL_PATH}/<message_recipient_id>',
        methods=['GET'],
        view_func=get_message_recipient,
        endpoint=get_message_recipient.__name__
    ),


@json_response(200)
@token_required
def list_message_recipients(current_user):
    return message_recipient_service.list_all()


@json_response(200)
@token_required
def get_message_recipient(current_user, message_recipient_id):
    return message_recipient_service.get(message_recipient_id)