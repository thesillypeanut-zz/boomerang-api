from src.validation.models import Event
from src.services import database_service


def create(event_instance):
    # for invitee in event_instance['invitees']:
    #     invitee_service.create(invitee)
    #
    # print(event_invitee_service.list_all())

    event_payload = {
        'name': event_instance['name'],
        'date': event_instance['date']
    }
    return database_service.post_entity_instance(Event, event_payload)


def delete(cart_id):
    cart = get(cart_id)
    if cart['is_ordered']:
        return f'Bad Request: You cannot delete cart with id "{cart_id}" that has an associated order.', 400

    return database_service.delete_entity_instance(Event, cart_id)


def get(cart_id, serialize=True):
    return database_service.get_entity_instance_by_id(Event, cart_id, serialize)


def list_all(filter_by):
    return database_service.get_entity_instances(Event, Event.date_created, filter_by)
