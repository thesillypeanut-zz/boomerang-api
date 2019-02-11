from flask import request

from constants import TWILIO_URL_PATH
from src.routes.decorators import json_response
from src.services import twilio_sms_service


def add_routes(app):
    app.add_url_rule(
        rule=f'{TWILIO_URL_PATH}/delivery',
        methods=['POST'],
        view_func=create_delivery_status,
        endpoint=create_delivery_status.__name__
    ),
    app.add_url_rule(
        rule=f'{TWILIO_URL_PATH}/responses/',
        methods=['POST'],
        view_func=save_response,
        endpoint=save_response.__name__
    ),
    app.add_url_rule(
        rule=f'{TWILIO_URL_PATH}/responses/',
        methods=['GET'],
        view_func=list_responses,
        endpoint=list_responses.__name__
    )


@json_response(201)
def create_delivery_status():
    pass


@json_response(201)
def save_response():
    return twilio_sms_service.save_response(request.form)


@json_response(200)
def list_responses():
    return twilio_sms_service.list_all()
