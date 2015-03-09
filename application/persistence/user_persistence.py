from application import db
from application.model.user import User

__author__ = 'Dani Meana'


def get(username):
    return User.query.get(username)


def save(user):
    db.session.add(user)
    db.session.commit()
