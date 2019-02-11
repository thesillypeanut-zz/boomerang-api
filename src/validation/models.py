from datetime import datetime
from sqlalchemy_utils import UUIDType

from src import db, bcrypt
from src.helpers import generate_uuid


class User(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    pwdhash = db.Column(db.String(80), nullable=False)
    events = db.relationship('Event', backref='organizer', lazy=True, cascade="all, delete-orphan, delete")
    messages = db.relationship('Message', backref='creator', lazy=True, cascade="all, delete-orphan, delete")

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwdhash, password)

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "events": [event.id for event in self.events],
            "messages": [message.id for message in self.messages]
        }


class Event(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    organizer_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'), nullable=False)
    event_invitees = db.relationship('EventInvitee', backref='event', lazy=True, secondary='', cascade="delete")

    def __repr__(self):
        return f"Event('{self.name}', '{self.date}', '{self.date_created}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "organizer_id": self.organizer_id,
            "date_created": self.date_created,
            "event_invitees": [item.id for item in self.event_invitees]
        }


class EventInvitee(db.Model):
    id = db.Column(UUIDType(binary=False), default=generate_uuid)
    date_invited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_id = db.Column(UUIDType(binary=False), db.ForeignKey('event.id'), primary_key=True, nullable=False)
    invitee_id = db.Column(UUIDType(binary=False), db.ForeignKey('invitee.id'), primary_key=True, nullable=False)
    message_recipients = db.relationship('MessageRecipient', backref='event_invitee', lazy=True, cascade="delete")

    def __repr__(self):
        return f"EventInvitee('{self.event_id}', '{self.invitee_id}', '{self.date_invited}')"

    def serialize(self):
        return {
            "id": self.id,
            "date_invited": self.date_invited,
            "event_id": self.event_id,
            "invitee_id": self.invitee_id,
            "message_recipients": [recipient.id for recipient in self.message_recipients]
        }


class MessageRecipient(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    date_received = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipient_id = db.Column(UUIDType(binary=False), db.ForeignKey('message_recipient.id'))
    recipient_group_id = db.Column(UUIDType(binary=False), db.ForeignKey('event_invitee.id'))
    message_id = db.Column(UUIDType(binary=False), db.ForeignKey('message.id'), nullable=False)

    def __repr__(self):
        return f"MessageRecipient('{self.event_id}', '{self.invitee_id}', '{self.date_received}')"

    def serialize(self):
        return {
            "id": self.id,
            "date_received": self.date_received,
            "recipient_id": self.recipient_id,
            "recipient_group_id": self.recipient_group_id,
            "message_id": self.message_id
        }


class Invitee(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    event_invitees = db.relationship('EventInvitee', backref='invitee', lazy=True, cascade="delete")
    message_recipients = db.relationship('MessageRecipient', backref='invitee', lazy=True, cascade="delete")

    def __repr__(self):
        return f"Invitee('{self.phone}', '{self.name}')"

    def serialize(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "name": self.name,
            "event_invitees": [item.id for item in self.event_invitees],
            "message_recipients": [recipient.id for recipient in self.message_recipients]
        }


class Message(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    sms_content = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    creator_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'), nullable=False)
    parent_message_id = db.Column(UUIDType(binary=False), db.ForeignKey('message.id'), nullable=True)
    message_recipients = db.relationship('MessageRecipient', backref='message', lazy=True, cascade="delete")

    def __repr__(self):
        return f"Message('{self.sms_content}', '{self.date_created}')"

    def serialize(self):
        return {
            "id": self.id,
            "sms_content": self.sms_content,
            "date_created": self.date_created,
            "creator_id": self.creator_id,
            "parent_message_id": self.parent_message_id,
            "message_recipients": [recipient.id for recipient in self.message_recipients]
        }
