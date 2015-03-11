from application import db

__author__ = 'Dani Meana'


class Rate(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'), primary_key=True)
    movie = db.relationship('Movie', backref=db.backref('rates'))
    user = db.relationship('User', backref=db.backref('rates'))
    value = db.Column(db.Float)

    def __init__(self, user, movie, value):
        self.user = user
        self.movie = movie
        self.value = value