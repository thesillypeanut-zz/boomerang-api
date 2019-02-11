from twilio.rest import Client

from constants import TWILIO_CALLBACK_PATH
from src.helpers import handle_exception
from src.services import message_service, invitee_service
from src.validation.models import Event, MessageRecipient

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
    # https://stackoverflow.com/questions/50075375/receiving-and-processing-an-sms-with-twilio-in-python
    message_id = response_form['MessageSid']
    from_number = response_form['From']
    body = response_form['Body'].strip().split(' ')
    response, event_code = body[0], body[1]

    # traverse down the db models
    event = Event.query.filter_by(event_code=event_code).first().serialize()
    recipient = None
    for event_invitee in event['event_invitees']:
        invitee = invitee_service.get(event_invitee['invitee_id'])
        if invitee['phone'] == from_number:
            recipient = {'recipient_id': event_invitee['invitee_id'], 'recipient_group_id': event_invitee['id']}
            break

    if not recipient:
        raise handle_exception('Incoming number could not be matched to an invitee for the specified event.', 500)

    message_recipient = MessageRecipient.query.filter_by(recipient_id=recipient['recipient_id']).first()
    if not message_recipient:
        message_recipient = MessageRecipient.query.filter_by(recipient_group_id=recipient['recipient_group_id']).first()

    message_recipient = message_recipient.serialize()
    message_recipient_message_id = message_recipient['message_id']
    message = message_service.get(message_recipient_message_id)
    message_service.create(message_id, response, message['creator_id'], message_recipient_message_id)
