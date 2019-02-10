from constants import DB_URL_PATH
from src.routes.decorators import json_response
from src.services import database_service


def add_routes(app):
    app.add_url_rule(
        rule=f'{DB_URL_PATH}/init',
        view_func=init_db,
        endpoint=init_db.__name__
    )


@json_response(204)
def init_db():
    return database_service.init()
