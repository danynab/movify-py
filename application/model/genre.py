from application import db

__author__ = 'Dani Meana'

genres = db.Table('genres',
                  db.Column('genre_name', db.Integer, db.ForeignKey('genre.name')),
                  db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
                  )


class Genre(db.Model):
    name = db.Column(db.String, primary_key=True)
    image = db.Column(db.String)
    movies = db.relationship('Movie', secondary=genres, backref=db.backref('genres'))

    def __init__(self, name, image):
        self.name = name
        self.image = image