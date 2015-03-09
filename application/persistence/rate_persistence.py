from application import db
from application.model.rate import Rate

__author__ = 'Dani Meana'


def get_by_movie(movie_id):
    return Rate.query.filter_by(movie_id=movie_id)


def save(rate):
    db.session.add(rate)
    db.session.commit()
