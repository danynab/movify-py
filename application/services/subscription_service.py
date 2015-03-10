from application.model.subscription import Subscription
from application.persistence import subscription_persistence

__author__ = 'Dani Meana'


def get_order_by_months():
    return subscription_persistence.get_order_by_months()


def save(name, description, months, price):
    subscription = Subscription(name, description, months, price)
    subscription_persistence.save(subscription)
    return subscription