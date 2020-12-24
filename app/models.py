from app import db


class AsDictMixin:
    def _key_values(self):
        columns = self.__table__.columns.keys()
        for col in columns:
            yield col, getattr(self, col)

    def as_dict(self):
        """Get the object as a dictionary
        """
        return dict(self._key_values())


class Entity(db.Model, AsDictMixin):
    """Entity Model"""
    id = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    balance = db.Column(db.Integer, db.CheckConstraint('balance>=0'), default=0)

    def __repr__(self):
        return '<Entity %r>' % self.name


class Transactions(db.Model, AsDictMixin):
    """Transactions Model"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String, db.ForeignKey('entity.id'), nullable=False)
    recipient_id = db.Column(db.String, db.ForeignKey('entity.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Transaction %r : %r>' % (self.id, self.amount)
