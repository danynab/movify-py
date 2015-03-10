from application import db

__author__ = 'Dani Meana'


class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email