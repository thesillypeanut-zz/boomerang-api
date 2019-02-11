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


@json_response(200)
@token_required
def list_messages(current_user):
    return message_service.list_all()