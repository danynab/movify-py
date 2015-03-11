from application import db
from application.model.review import Review

__author__ = 'Dani Meana'


def get_by_movie_id(movie_id):
    return Review.query.filter_by(movie_id=movie_id)


def save(review):
    db.session.add(review)
    db.session.commit()
