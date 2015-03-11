from application import db
from application.model.movie import Movie

__author__ = 'Dani Meana'


def get(movie_id):
    return Movie.query.get(movie_id)


def get_all():
    return Movie.query.all()


def find_by_title(title):
    return Movie.query.filter(Movie.title.ilike('%' + title + '%')).all()


def find_by_category(category):
    return Movie.query.filter(Movie.categories.ilike('%' + category + '%')).all()


def save(movie):
    db.session.add(movie)
    db.session.commit()
