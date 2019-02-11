from src.validation.models import EventInvitee
from src.services import database_service, invitee_service


def list_all():
    return database_service.get_entity_instances(EventInvitee)
