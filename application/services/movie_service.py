from application.model.movie import Movie
from application.persistence import movie_persistence
from application.services import review_service, genre_service
import random

__author__ = 'Dani Meana'


def get(movie_id):
    return movie_persistence.get(movie_id)


def get_all():
    return movie_persistence.get_all()


def get_random(count):
    ids = [movie.id for movie in get_all()]
    return [get(movie_id) for movie_id in random.sample(ids, count)]


def search(text):
    return movie_persistence.search(text)


def save(title, year, duration, genres, description, storyline, director, writers, stars, cover, background, movie,
         trailer):
    movie = Movie(title, year, duration, genres, description, storyline, director, writers, stars, cover,
                  background, movie, trailer)
    movie_persistence.save(movie)
    return movie


def movie_to_dict(movie):
    if movie.reviews.__len__() > 0:
        rating = int((sum([review.rating for review in movie.reviews]) / movie.reviews.__len__()) * 100) / 100.0
    else:
        rating = 0
    _dict = {'id': movie.id,
             'title': movie.title,
             'year': movie.year,
             'duration': movie.duration,
             'genres': genre_service.genres_to_dicts(movie.genres, add_movies=False),
             'description': movie.description,
             'storyline': movie.storyline,
             'director': movie.director,
             'writers': movie.writers,
             'stars': movie.stars,
             'cover': movie.cover,
             'background': movie.background,
             'movie': movie.movie,
             'trailer': movie.trailer,
             'reviews': review_service.reviews_to_dicts(movie.reviews),
             'rating': rating}
    return {k: v for k, v in _dict.items() if v is not None}


def movies_to_dicts(movies):
    return [movie_to_dict(movie) for movie in movies]
