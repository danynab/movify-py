from application import db

__author__ = 'Dani Meana'


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    # categories
    description = db.Column(db.String)
    storyline = db.Column(db.String)
    director = db.Column(db.String)
    writers = db.Column(db.String)
    stars = db.Column(db.String)
    cover = db.Column(db.String)
    background = db.Column(db.String)

    def __init__(self, title, year, duration, description, storyline, director, writers, stars, cover, background):
        self.title = title
        self.year = year
        self.duration = duration
        self.description = description
        self.storyline = storyline
        self.director = director
        self.writers = writers
        self.stars = stars
        self.cover = cover
        self.background = background

    def to_dict(self):
        _dict = {'title': self.title,
                 'year': self.year,
                 'duration': self.duration,
                 'description': self.description,
                 'storyline': self.storyline,
                 'director': self.director,
                 'writers': self.writers,
                 'stars': self.stars,
                 'cover': self.cover,
                 'background': self.background}
        return {k: v for k, v in _dict.items() if v}