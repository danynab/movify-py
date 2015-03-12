from application.model.review import Review
from application.persistence import review_persistence

__author__ = 'Dani Meana'


def get_by_movie_id(movie_id):
    return review_persistence.get_by_movie_id(movie_id)


def get_by_movie_id_and_username(movie_id, username):
    return review_persistence.get_by_movie_id_and_username(movie_id, username)


def rate_movie(user, movie, rating, comment):
    review = Review(user, movie, rating, comment)
    review_persistence.save(review)
    return review


def review_to_dict(review):
    _dict = {'username': review.user.username,
             'rating': review.rating,
             'comment': review.comment}
    return {k: v for k, v in _dict.items() if v is not None}


def reviews_to_dicts(reviews):
    return [review_to_dict(review) for review in reviews]