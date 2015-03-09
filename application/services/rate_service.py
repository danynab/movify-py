from application.model.rate import Rate
from application.persistence import rate_persistence
from application.services import movie_service, user_service

__author__ = 'Dani Meana'


def rate_movie(movie_id, username, value):
    movie = movie_service.get(movie_id)
    user = user_service.get(username)
    rate = Rate(user, movie, value)
    return rate_persistence.save(rate)