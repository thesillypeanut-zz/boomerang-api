from src.validation.models import Message
from src.services import database_service


def create(id, body, creator_id, parent_message_id=None):
    message_payload = {'sms_content': body, 'creator_id': creator_id, 'id': id}
    if parent_message_id:
        message_payload['parent_message_id'] = parent_message_id

    return database_service.post_entity_instance(Message, message_payload)


def get(message_id):
    return database_service.get_entity_instance_by_id(Message, message_id)


def list_all(filter_by):
    return database_service.get_entity_instances(Message, filter_by=filter_by)