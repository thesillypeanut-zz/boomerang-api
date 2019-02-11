from src.validation.models import Invitee
from src.services import database_service


def create(invitee_instance):
    return database_service.post_entity_instance(Invitee, invitee_instance)


def get(invitee_id):
    return database_service.get_entity_instance_by_id(Invitee, invitee_id)
