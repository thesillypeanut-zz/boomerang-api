import logging
from werkzeug import exceptions

from src import db
from src.helpers import handle_exception

logger = logging.getLogger(__name__)


def delete_entity_instance(db_model, entity_id, is_id_primary_key=True):
    try:
        entity = (
            db_model.query.get_or_404(entity_id)
            if is_id_primary_key else
            db_model.query.filter_by(id=entity_id).first()
        )
    except exceptions.NotFound:
        raise handle_exception(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.', 404)

    db.session.delete(entity)
    db.session.commit()
    return '', 204


def edit_entity_instance(db_model, entity_id, updated_entity_instance, is_id_primary_key=True):
    try:
        entity = (
            db_model.query.get_or_404(entity_id)
            if is_id_primary_key else
            db_model.query.filter_by(id=entity_id).first()
        )
    except exceptions.NotFound:
        raise handle_exception(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.', 404)

    for key in updated_entity_instance:
        setattr(entity, key, updated_entity_instance[key])

    db.session.commit()

    return entity.serialize()


def get_entity_instances(db_model, order_by=None, filter_by=None):
    try:
        if filter_by:
            entities = (
                db_model.query.order_by(order_by).filter_by(**filter_by.to_dict()).all()
                if type(filter_by) != dict else db_model.query.order_by(order_by).filter_by(**filter_by).all()
            )
        else:
            entities = db_model.query.order_by(order_by).all()
    except Exception:
        raise handle_exception(f'Exception encountered while querying "{db_model.__name__}" ordered by "{order_by}" '
                     f'filtered by "{filter_by}".')

    return [entity.serialize() for entity in entities]


def get_entity_instance_by_id(db_model, entity_id, serialize=True, is_id_primary_key=True):
    try:
        entity = (
            db_model.query.get_or_404(entity_id)
            if is_id_primary_key else
            db_model.query.filter_by(id=entity_id).first()
        )

    except exceptions.NotFound:
        raise handle_exception(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.', 404)

    if not serialize:
        return entity

    return entity.serialize()


def init():
    db.drop_all()
    db.create_all()
    return '', 204


def post_entity_instance(db_model, entity_instance=None):
    entity = db_model(**entity_instance) if entity_instance else db_model()
    db.session.add(entity)
    db.session.commit()

    return entity.serialize()
