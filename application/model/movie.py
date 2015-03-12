from application import db

__author__ = 'Dani Meana'


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    genres = db.Column(db.String)
    description = db.Column(db.String)
    storyline = db.Column(db.String)
    director = db.Column(db.String)
    writers = db.Column(db.String)
    stars = db.Column(db.String)
    cover = db.Column(db.String)
    background = db.Column(db.String)
    movie = db.Column(db.String)
    trailer = db.Column(db.String)

    def __init__(self, title, year, duration, genres, description, storyline, director, writers, stars, cover,
                 background, movie, trailer):
        self.title = title
        self.year = year
        self.duration = duration
        self.genres = genres
        self.description = description
        self.storyline = storyline
        self.director = director
        self.writers = writers
        self.stars = stars
        self.cover = cover
        self.background = background
        self.movie = movie
        self.trailer = trailer