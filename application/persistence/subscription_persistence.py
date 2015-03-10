from application import db
from application.model.subscription import Subscription

__author__ = 'Dani Meana'


def get_order_by_months():
    return Subscription.query.order_by(Subscription.months).all()


def save(subscription):
    db.session.add(subscription)
    db.session.commit()