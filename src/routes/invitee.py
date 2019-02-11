from constants import INVITEE_URL_PATH
from src.routes.decorators import json_response, token_required
from src.services import invitee_service


def add_routes(app):
    app.add_url_rule(
        rule=f'{INVITEE_URL_PATH}/',
        methods=['GET'],
        view_func=list_invitees,
        endpoint=list_invitees.__name__
    ),
    app.add_url_rule(
        rule=f'{INVITEE_URL_PATH}/<invitee_id>',
        methods=['GET'],
        view_func=get_invitee,
        endpoint=get_invitee.__name__
    ),


@json_response(200)
@token_required
def list_invitees(current_user):
    return invitee_service.list_all()


@json_response(200)
@token_required
def get_invitee(current_user, invitee_id):
    return invitee_service.get(invitee_id)