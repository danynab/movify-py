from application import db
from application.model.movie import Movie

__author__ = 'Dani Meana'


def get(movie_id):
    return Movie.query.get(movie_id)


def get_all():
    return Movie.query.all()


def save(movie):
    db.session.add(movie)
    db.session.commit()