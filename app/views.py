import flask
from sqlalchemy.exc import IntegrityError

from . import app, db
from . import models


class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict(
            error='error processing request',
            message=self.message)
        return rv


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    """Convert invalid usage errors to json responses"""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/api/entity/<entityid>/transactions', methods=['GET'])
def entity_transactions(entityid):
    """
    To-Do:
    Return a list of all transactions for a specific entity
    """
    return flask.jsonify([])


@app.route('/api/transaction', methods=['POST'])
def process_transaction():
    trans_amount = flask.request.json['amount']
    sender_id = flask.request.json['sender']
    recipient_id = flask.request.json['recipient']

    sender = models.Entity.query \
        .get(sender_id)
    recipient = models.Entity.query \
        .get(recipient_id)

    if not sender or not recipient:
        raise InvalidAPIUsage("user does not exist", status_code=400)

    trans = models.Transactions(
        sender_id=sender.id,
        recipient_id=recipient.id,
        amount=trans_amount
    )
    try:
        sender.balance -= trans_amount
        recipient.balance += trans_amount
        db.session.add(trans)
        db.session.commit()
    except IntegrityError:
        raise InvalidAPIUsage('invalid transaction', status_code=400)

    return flask.jsonify(success=True)


@app.route('/api/entity', methods=['POST'])
def add_entity():
    userid = flask.request.json['userid']
    password = flask.request.json['password']
    initial_balance = flask.request.json.get('initial_balance', 0)
    entity = models.Entity(
        id=userid,
        password=password,
        balance=initial_balance)
    db.session.add(entity)
    try:
        db.session.commit()
    except IntegrityError:
        raise InvalidAPIUsage('entity exists', status_code=409)
    return flask.jsonify(entity.as_dict())


@app.route('/api/entity', methods=['GET'])
def get_entitys():
    """Get a JSON list of entitys"""
    entitys = models.Entity.query.all()
    entity_list = [u.as_dict() for u in entitys]
    return flask.jsonify(entity_list)
