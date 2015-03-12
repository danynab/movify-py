from application import db
from application.model.movie import Movie

__author__ = 'Dani Meana'


def get(movie_id):
    return Movie.query.get(movie_id)


def get_all():
    return Movie.query.all()


def search(text):
    condition = '%' + text + '%'
    return Movie.query.filter(Movie.title.ilike(condition) |
                              Movie.director.ilike(condition) |
                              Movie.writers.ilike(condition) |
                              Movie.stars.ilike(condition)).all()


def save(movie):
    db.session.add(movie)
    db.session.commit()
