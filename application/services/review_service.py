from application.model.review import Review
from application.persistence import review_persistence

__author__ = 'Dani Meana'


def get_by_movie_id(movie_id):
    return review_persistence.get_by_movie_id(movie_id)


def rate_movie(movie, user, rate, comment):
    review = Review(user, movie, rate, comment)
    return review_persistence.save(review)


def review_to_dict(review):
    _dict = {'rate': review.rate,
             'comment': review.comment}
    return {k: v for k, v in _dict.items() if v is not None}


def reviews_to_dicts(reviews):
    return [review_to_dict(review) for review in reviews]