from application import app, prefix
from flask import redirect, request, render_template, url_for
from application.services import user_service, movie_service, rate_service

__author__ = 'Dani Meana'


@app.after_request
def print_ip(response):
    try:
        ip = request.headers.environ['HTTP_X_FORWARDED_FOR']
    except KeyError:
        ip = 'NO-IP'
    user_agent = request.headers.environ['HTTP_USER_AGENT']
    print()
    print(('IP: ' + ip if ip else 'None') + ((' - UserAgent: ' + user_agent) if user_agent else ''))
    return response


@app.route(prefix + "/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route(prefix + "/init")
def init():
    from application import db

    db.drop_all()
    db.create_all()
    return "Tables created"


# Users

@app.route(prefix + "/login", methods=["GET"])
def show_login():
    return render_template('login.html')


@app.route(prefix + "/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]
    user = user_service.login(username, password)
    if user is not None:
        return 'Login successful'
    else:
        return 'Username or password is not correct'


@app.route(prefix + "/signup", methods=["GET"])
def show_register():
    return render_template('signup.html')


@app.route(prefix + "/signup", methods=["POST"])
def do_register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    confirm_email = request.form["confirm_email"]
    if username.__len__() == 0:
        return "Username can not be empty"
    if password.__len__() == 0:
        return "Password can not be empty"
    if email.__len__() == 0:
        return "Email can not be empty"
    if email == confirm_email:
        user = user_service.register(username, password, email)
        return "Success. User registered" if user is not None else "Username already registered"
    else:
        return "Emails not equals"


# Movies

@app.route(prefix + "/movies", methods=["GET"])
def show_movies():
    movies = movie_service.get_all()
    return render_template('util.html', movies=movies)


@app.route(prefix + "/movies", methods=["POST"])
def save_movie():
    title = request.form["title"]
    synopsis = request.form["synopsis"]
    year = request.form["year"]
    time = request.form["time"]
    director = request.form["director"]
    cast = request.form["cast"]
    genre = request.form["genre"]
    url = request.form["url"]
    cover = request.form["cover"]
    movie = movie_service.save(title, synopsis, year, time, director, cast, genre, url, cover)
    return redirect(url_for("show_movies"))


@app.route(prefix + "/movies/<int:movie_id>/rates", methods=["POST"])
def rate_movie(movie_id):
    value = request.form["value"]
    users = user_service.get_all()
    user = users[users.__len__()-1]
    rate = rate_service.rate_movie(movie_id, user.username, value)
    return redirect(url_for("show_movies"))


# UTIL

@app.route(prefix + "/util", methods=["GET"])
def show_util():
    movies = movie_service.get_all()
    return render_template('util.html', movies=movies)
