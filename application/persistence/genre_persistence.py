from application import db
from application.model.genre import Genre

__author__ = 'Dani Meana'


def get(name):
    return Genre.query.get(name)


def get_all():
    return Genre.query.all()


def save(genre):
    db.session.add(genre)
    db.session.commit()
