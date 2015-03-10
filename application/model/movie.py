from application import db

__author__ = 'Dani Meana'


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    synopsis = db.Column(db.String)
    year = db.Column(db.Integer)
    time = db.Column(db.BigInteger)
    director = db.Column(db.String)
    cast = db.Column(db.String)
    genre = db.Column(db.String)
    url = db.Column(db.String)
    cover = db.Column(db.String)

    def __init__(self, title, synopsis, year, time, director, cast, genre, url, cover):
        self.title = title
        self.synopsis = synopsis
        self.year = year
        self.time = time
        self.director = director
        self.cast = cast
        self.genre = genre
        self.url = url
        self.cover = cover