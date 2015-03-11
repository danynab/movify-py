from application.model.movie import Movie
from application.persistence import movie_persistence

__author__ = 'Dani Meana'


def get(movie_id):
    return movie_persistence.get(movie_id)


def get_all():
    return movie_persistence.get_all()


def save(title, year, duration, description, storyline, director, writers, stars, cover, background):
    movie = Movie(title, year, duration, description, storyline, director, writers, stars, cover, background)
    movie_persistence.save(movie)
    return movie