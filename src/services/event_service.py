from datetime import datetime

from src.validation.models import Event
from src.services import (
    database_service,
    invitee_service,
    event_invitee_service,
    message_recipient_service,
    twilio_sms_service,
)


def create(event_instance, current_user):
    def _create_event(current_user_id):
        event_payload = {
            'name': event_instance['name'],
            'date': datetime.strptime(event_instance['date'], '%b %d %Y %I:%M%p'),
            'organizer_id': current_user_id,
        }
        return database_service.post_entity_instance(Event, event_payload)

    def _create_invitees_and_message(event_code):
        for invitee in event_instance['invitees']:
            invitee = invitee_service.create(invitee)
            event_invitee = event_invitee_service.create(event['id'], invitee['id'])

            sms_body = f'{current_user.first_name} {current_user.last_name} has invited you to ' \
                       f'{event_instance["name"]} on {event_instance["date"]}\n{event_instance["sms_content"]}\n' \
                       f'RSVP with "yes {event_code}" or "no {event_code}".'
            message_id = twilio_sms_service.send_sms(invitee['phone'], sms_body, current_user.id)
            message_recipient_service.create(message_id, recipient_group_id=event_invitee['id'])


    current_user_id = current_user.id
    event = _create_event(current_user_id)
    _create_invitees_and_message(event['event_code'])

    return event


def update(event_id, event_instance):
    pass


def delete(event_id):
    return database_service.delete_entity_instance(Event, event_id)


def get(event_id, serialize=True):
    return database_service.get_entity_instance_by_id(Event, event_id, serialize)


def get_by_event_code(event_code, serialize=True):
    return database_service.get_entity_instance_by_id(Event, event_code, serialize)


def list_all(filter_by):
    return database_service.get_entity_instances(Event, Event.date_created, filter_by)
