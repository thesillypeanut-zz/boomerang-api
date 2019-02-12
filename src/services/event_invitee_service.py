from src.validation.models import EventInvitee
from src.services import database_service


def list_all():
    return database_service.get_entity_instances(EventInvitee)


def get(event_invitee_id):
    return database_service.get_entity_instance_by_id(EventInvitee, event_invitee_id, is_id_primary_key=False)


def create(event_id, invitee_id):
    return database_service.post_entity_instance(EventInvitee, {'event_id': event_id, 'invitee_id': invitee_id})
