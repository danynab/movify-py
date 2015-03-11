from application.model.movie import Movie
from application.persistence import movie_persistence

__author__ = 'Dani Meana'


def get(movie_id):
    return movie_persistence.get(movie_id)


def get_all():
    return movie_persistence.get_all()


def find_by_title(title):
    return movie_persistence.find_by_title(title)


def save(title, year, duration, categories, description, storyline, director, writers, stars, cover, background):
    movie = Movie(title, year, duration, categories, description, storyline, director, writers, stars, cover,
                  background)
    movie_persistence.save(movie)
    return movie


def movie_to_dict(movie):
    categories = movie.categories.split(',')
    _dict = {'title': movie.title,
             'year': movie.year,
             'duration': movie.duration,
             'categories': categories,
             'description': movie.description,
             'storyline': movie.storyline,
             'director': movie.director,
             'writers': movie.writers,
             'stars': movie.stars,
             'cover': movie.cover,
             'background': movie.background}
    return {k: v for k, v in _dict.items() if v}


def movies_to_dicts(movies):
    return [movie_to_dict(movie) for movie in movies]