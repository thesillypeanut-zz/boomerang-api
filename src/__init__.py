from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config


db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_name):
    from src.validation.models import User, Event, EventInvitee, Invitee, Message, MessageRecipient

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    # db.drop_all(app=app)
    # db.create_all(app=app)

    from src.routes import user, database, event
    user.add_routes(app)
    database.add_routes(app)
    event.add_routes(app)

    return app
