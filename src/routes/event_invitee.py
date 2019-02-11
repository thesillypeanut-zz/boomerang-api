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
    app.add_url_rule(
        rule=f'{EVENT_INVITEE_URL_PATH}/<event_invitee_id>',
        methods=['GET'],
        view_func=get_event_invitee,
        endpoint=get_event_invitee.__name__
    ),


@json_response(200)
@token_required
def list_event_invitees(current_user):
    return event_invitee_service.list_all()


@json_response(200)
@token_required
def get_event_invitee(current_user, event_invitee_id):
    return event_invitee_service.get(event_invitee_id)