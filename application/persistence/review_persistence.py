from application import db
from application.model.review import Review

__author__ = 'Dani Meana'


def get_by_movie_id(movie_id):
    return Review.query.filter_by(movie_id=movie_id)


def get_by_movie_id_and_username(movie_id, username):
    return Review.query.filter_by(movie_id=movie_id).filter_by(username=username).first()


def save(review):
    db.session.add(review)
    db.session.commit()
