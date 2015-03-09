from application import app
from flask import redirect

__author__ = 'Dani Meana'


@app.route("/", methods=["GET"])
def hello():
    return redirect("https://github.com/danynab/movify-py")