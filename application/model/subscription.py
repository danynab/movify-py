from application import db

__author__ = 'Dani Meana'


class Subscription(db.Model):
    name = db.Column(db.String)
    description = db.Column(db.String)
    months = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)

    def __init__(self, name, description, months, price):
        self.name = name
        self.description = description
        self.months = months
        self.price = price