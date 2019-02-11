from src.validation.models import MessageRecipient
from src.services import database_service


def create(message_id, recipient_id=None, recipient_group_id=None):
    if recipient_group_id:
        return database_service.post_entity_instance(
            MessageRecipient, {'message_id': message_id, 'recipient_group_id': recipient_group_id}
        )

    if recipient_id:
        return database_service.post_entity_instance(
            MessageRecipient, {'message_id': message_id, 'recipient_id': recipient_id}
        )


def list_all():
    return database_service.get_entity_instances(MessageRecipient)


def get(message_recipient_id):
    return database_service.get_entity_instance_by_id(MessageRecipient, message_recipient_id)