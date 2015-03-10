from functools import wraps
from application import app, prefix
from flask import redirect, request, render_template, url_for, session, g
from application.services import user_service, movie_service, rate_service
import hashlib

__author__ = 'Dani Meana'

SESSION_ID_KEY = "session_id"
USERNAME_KEY = "username"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if SESSION_ID_KEY in session and USERNAME_KEY in session:
            session_id = session[SESSION_ID_KEY]
            username = session[USERNAME_KEY]
            if session_id == _calculate_session_id():
                user = user_service.get(username)
                if user is not None:
                    return f(*args, **kwargs)
        return redirect(url_for('show_login'))
    return decorated_function


def _calculate_session_id():
    ip = g.get("ip", "")
    user_agent = g.get("user_agent", "")
    session_id_str = ip + user_agent
    return _to_md5(_to_md5(session_id_str))


def _to_md5(string):
    return hashlib.md5(string.encode("utf")).hexdigest()


@app.before_request
def print_ip():
    try:
        ip = request.headers.environ['HTTP_X_FORWARDED_FOR']
    except KeyError:
        try:
            ip = request.headers.environ['REMOTE_ADDR']
        except KeyError:
            ip = None
    if not ip:
        ip = 'NO IP'
    user_agent = request.headers.environ['HTTP_USER_AGENT']
    print()
    print(('IP: ' + ip if ip else 'None') + ((' - UserAgent: ' + user_agent) if user_agent else ''))
    g.ip = ip
    g.user_agent = user_agent


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
        session_id = _calculate_session_id()
        session[SESSION_ID_KEY] = session_id
        session[USERNAME_KEY] = username
        return redirect(url_for("index"))
    else:
        return redirect(url_for("show_login"))


@app.route(prefix + "/logout", methods=["GET"])
@login_required
def do_logout():
    session.pop(SESSION_ID_KEY)
    session.pop(USERNAME_KEY)
    return redirect(url_for("index"))


@app.route(prefix + "/signup", methods=["GET"])
def show_signup():
    return render_template('signup.html')


@app.route(prefix + "/signup", methods=["POST"])
def do_signup():
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
        if user is not None:
            session_id = _calculate_session_id()
            session[SESSION_ID_KEY] = session_id
            session[USERNAME_KEY] = user.username
            return redirect(url_for("index"))
        return "Username already registered"
    else:
        return "Emails not equals"


# Account

@app.route(prefix + "/account", methods=["GET"])
@login_required
def show_account():
    return render_template('account.html')

# Movies

@app.route(prefix + "/movies", methods=["GET"])
@login_required
def show_movies():
    movies = movie_service.get_all()
    return render_template('util.html', movies=movies)


@app.route(prefix + "/movies", methods=["POST"])
@login_required
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
@login_required
def rate_movie(movie_id):
    value = request.form["value"]
    users = user_service.get_all()
    user = users[users.__len__() - 1]
    rate = rate_service.rate_movie(movie_id, user.username, value)
    return redirect(url_for("show_movies"))


# UTIL

@app.route(prefix + "/util", methods=["GET"])
@login_required
def show_util():
    movies = movie_service.get_all()
    return render_template('util.html', movies=movies)