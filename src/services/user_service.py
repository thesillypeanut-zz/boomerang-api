import jwt
import logging
from datetime import datetime, timedelta

from instance.config import Config
from src.models import User
from src.services import database_service

logger = logging.getLogger(__name__)


def create(user_instance):
    return database_service.post_entity_instance(User, user_instance)


def delete(user_id):
    return database_service.delete_entity_instance(User, user_id)


def update(user_id, user_instance):
    return database_service.edit_entity_instance(User, user_id, user_instance)


def get(user_id):
    return database_service.get_entity_instance_by_id(User, user_id)


def list_all():
    return database_service.get_entity_instances(User)


def login(auth):
    if not auth or not auth.username or not auth.password:
        return 'Unauthorized: Could not verify user.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    user = User.query.filter_by(email=auth.username).first()
    if not user or not user.check_password(auth.password):
        return 'Unauthorized: Incorrect email and/or password.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    token = jwt.encode(
        {'id': str(user.id), 'exp': datetime.utcnow() + timedelta(hours=1)},
        Config.SECRET_KEY
    )
    return {'token': token.decode('UTF-8')}
