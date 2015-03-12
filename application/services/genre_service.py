from application import services
from application.model.genre import Genre
from application.persistence import genre_persistence

__author__ = 'Dani Meana'


def get(name):
    return genre_persistence.get(name)


def get_all():
    return genre_persistence.get_all()


def get_movies(name):
    genre = get(name)
    return genre.movies


def save(name, image):
    genre = Genre(name, image)
    genre_persistence.save(genre)
    return genre


def genre_to_dict(genre, add_movies=True):
    _dict = {'name': genre.name,
             'image': genre.image,
             'movies': services.movie_service.movies_to_dicts(genre.movies) if add_movies is True else None}
    return {k: v for k, v in _dict.items() if v is not None}


def genres_to_dicts(genres, add_movies=True):
    return [genre_to_dict(genre, add_movies=add_movies) for genre in genres]
