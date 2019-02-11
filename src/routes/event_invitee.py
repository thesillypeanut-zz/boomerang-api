from constants import EVENT_INVITEE_URL_PATH
from src.routes.decorators import json_response, token_required
from src.services import event_invitee_service


def add_routes(app):
    app.add_url_rule(
        rule=f'{EVENT_INVITEE_URL_PATH}/',
        methods=['GET'],
        view_func=list_event_invitees,
        endpoint=list_event_invitees.__name__
    ),


@json_response(200)
@token_required
def list_event_invitees(current_user):
    return event_invitee_service.list_all()