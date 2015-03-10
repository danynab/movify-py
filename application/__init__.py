from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

__author__ = 'Dani Meana'

prefix = "/movify"

app = Flask(__name__, static_path=prefix + "/static")
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/movify.db'
db = SQLAlchemy(app)

import application.controller