from application import db

__author__ = 'Dani Meana'


class Review(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'), primary_key=True)
    movie = db.relationship('Movie', backref=db.backref('reviews'))
    user = db.relationship('User', backref=db.backref('reviews'))
    rate = db.Column(db.Float)
    comment = db.Column(db.String)

    def __init__(self, user, movie, rate, comment):
        self.user = user
        self.movie = movie
        self.rate = rate
        self.comment = comment