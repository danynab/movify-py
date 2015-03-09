from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

__author__ = 'Dani Meana'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/movify.db'
db = SQLAlchemy(app)

import application.controller