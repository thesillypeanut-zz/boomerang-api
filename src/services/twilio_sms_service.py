from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from constants import TWILIO_CALLBACK_PATH
from src.helpers import handle_exception
from src.services import message_service, invitee_service, database_service
from src.validation.models import Event, MessageRecipient, Message

client = Client('ACdc8ff33a38fa6e0055a4720ef13f7e6c', 'b9854bf8857fe3edfa9905f2a6ca8f24')
TWILIO_PHONE_NUM = '+16479314760'


def send_sms(phone_num, sms_body, creator_id):
    message = client.messages.create(
        from_=TWILIO_PHONE_NUM,
        body=sms_body,
        to=phone_num,
        status_callback=TWILIO_CALLBACK_PATH
    )
    print(message.sid)
    message_id = message.sid
    message_service.create(message_id, sms_body, creator_id)
    return message_id


def save_response(response_form):
    def _find_event_and_get_recipient_id_object(event_code, from_number):
        event = Event.query.filter_by(event_code=event_code).first().serialize()

        for event_invitee in event['event_invitees']:
            # recipient must be one of the event invitees
            invitee = invitee_service.get(event_invitee['invitee_id'])
            if invitee['phone'] == from_number:
                return {'recipient_id': event_invitee['invitee_id'], 'recipient_group_id': event_invitee['id']}

        return None

    def _find_message_recipient_and_get_parent_message_id(recipient_id_object):
        message_recipient = MessageRecipient.query.filter_by(recipient_id=recipient_id_object['recipient_id']).first()

        if not message_recipient:
            message_recipient = MessageRecipient.query.filter_by(
                recipient_group_id=recipient_id_object['recipient_group_id']
            ).first()

        message_recipient = message_recipient.serialize()
        return message_recipient['message_id']


    # https://stackoverflow.com/questions/50075375/receiving-and-processing-an-sms-with-twilio-in-python
    from_number = response_form['From']
    body = response_form['Body'].strip().split(' ')
    response, event_code = body[0], body[1]

    recipient_id_object = _find_event_and_get_recipient_id_object(event_code, from_number)

    if not recipient_id_object:
        raise handle_exception('Incoming number could not be matched to an invitee for the specified event.', 500)

    parent_message_id = _find_message_recipient_and_get_parent_message_id(recipient_id_object)
    parent_message = message_service.get(parent_message_id)
    message_service.create(response_form['MessageSid'], response, parent_message['creator_id'], parent_message_id)

    resp = MessagingResponse()
    resp.message("Your response was saved!")

    return str(resp)


def list_all():
    return database_service.get_entity_instances(Message)