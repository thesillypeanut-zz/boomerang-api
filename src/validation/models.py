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
            "events": [{"event_id": event.id} for event in self.events]
        }


class Event(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    organizer_id = db.Column(UUIDType(binary=False), db.ForeignKey('user.id'), nullable=False)
    # cart_items = db.relationship('CartItem', backref='cart', lazy=True, cascade="delete")
    # order = db.relationship('Order', backref='cart', lazy=True)

    def __repr__(self):
        return f"Event('{self.name}', '{self.date}', '{self.date_created}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "organizer_id": self.organizer_id,
            "date_created": self.date_created,
            # "cart_item_ids": [item.id for item in self.cart_items],
            # "is_ordered": True if self.order else False
        }
#
#
# class Product(db.Model):
#     id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
#     title = db.Column(db.String(120), nullable=False)
#     price = db.Column(db.Float(), nullable=False)
#     inventory_count = db.Column(db.Integer(), nullable=False)
#     cart_items = db.relationship('CartItem', backref='product', lazy=True)
#
#     def __repr__(self):
#         return f"Product('{self.title}', '{self.price}', '{self.inventory_count}')"
#
#     def serialize(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "price": self.price,
#             "inventory_count": self.inventory_count,
#             "cart_item_ids": [item.id for item in self.cart_items]
#         }
#
#
# class CartItem(db.Model):
#     id = db.Column(UUIDType(binary=False), default=generate_uuid)
#     date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     quantity = db.Column(db.Integer(), nullable=False)
#     cart_id = db.Column(UUIDType(binary=False), db.ForeignKey('cart.id'), primary_key=True, nullable=False)
#     product_id = db.Column(UUIDType(binary=False), db.ForeignKey('product.id'), primary_key=True, nullable=False)
#
#     def __repr__(self):
#         return f"CartItem('{self.id}', '{self.cart_id}', '{self.product_id}', '{self.date_added}', '{self.quantity}')"
#
#     def serialize(self):
#         return {
#             "id": self.id,
#             "quantity": self.quantity,
#             "date_added": self.date_added,
#             "cart_id": self.cart_id,
#             "product_id": self.product_id
#         }
#
#
# class Order(db.Model):
#     id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
#     cart_id = db.Column(UUIDType(binary=False), db.ForeignKey('cart.id'))
#     date_ordered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     subtotal = db.Column(db.Float(), nullable=False)
#
#     def __repr__(self):
#         return f"Order(''{self.cart_id}', '{self.date_ordered}', '{self.subtotal}')"
#
#     def serialize(self):
#         return {
#             "id": self.id,
#             "cart_id": self.cart_id,
#             "date_ordered": self.date_ordered,
#             "subtotal": self.subtotal
#         }
