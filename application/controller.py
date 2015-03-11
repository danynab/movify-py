from application.payments.cajastur import cajastur_payment
from application.payments.paypal import paypal_payment
from flask.json import dumps
from datetime import datetime
from functools import wraps
from application import app, prefix
from flask import redirect, request, render_template, url_for, session, g, Response
from application.services import user_service, movie_service, rate_service, subscription_service
import hashlib

__author__ = 'Dani Meana'

SESSION_ID_KEY = "session_id"
USERNAME_KEY = "username"
PAYPAL_ID_KEY = "paypal_id"


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


def _generate_product_name(months):
    date_now = datetime.now()
    date_now_str = str(date_now.year) + str(date_now.month) + str(date_now.day) + str(date_now.hour) + str(
        date_now.minute) + str(date_now.second)
    return "Movify" + str(months) + "m" + date_now_str


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
    import application.data as data
    from application import db

    db.drop_all()
    db.create_all()

    for subscription in data.subscriptions:
        subscription_service.save(
            name=subscription["name"],
            description=subscription["description"],
            months=subscription["months"],
            price=subscription["price"])

    for movie in data.movies:
        movie_service.save(
            title=movie["title"],
            year=movie["year"],
            duration=movie["duration"],
            description=movie["description"],
            storyline=movie["storyline"],
            director=movie["director"],
            writers=movie["writers"],
            stars=movie["stars"],
            cover="http://156.35.95.67/movify/static/covers/" + movie["cover"],
            background="http://156.35.95.67/movify/static/background/" + movie["background"]
        )

    user_service.signup("dani", "dani", "dani@danynab.es")

    return redirect(url_for("index"))


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
        user = user_service.signup(username, password, email)
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
    subscriptions = subscription_service.get_order_by_months()
    return render_template('account.html', subscriptions=subscriptions)


@app.route(prefix + "/_generate_cajastur_payment_data")
@login_required
def generate_cajastur_payment_data():
    months = request.args.get("months", 0, type=int)
    subscription = subscription_service.get_by_months(months)
    if subscription is None:
        return redirect(url_for("index"))
    else:
        return_url = "http://156.35.95.67/movify/account/subscription/cajastur"
        cancel_url = "http://156.35.95.67/movify/account"
        cajastur_data = _get_cajastur_payment_data(subscription, return_url, cancel_url)
        return dumps(cajastur_data)


@app.route(prefix + "/_generate_paypal_payment_data")
@login_required
def generate_paypal_payment_data():
    months = request.args.get("months", 0, type=int)
    subscription = subscription_service.get_by_months(months)
    if subscription is None:
        return redirect(url_for("index"))
    else:
        return_url = "http://156.35.95.67/movify/account/subscription/paypal"
        cancel_url = "http://156.35.95.67/movify/account"
        paypal_data = _get_paypal_payment_data(subscription, return_url, cancel_url)
        return dumps(paypal_data)


def _get_paypal_payment_data(subscription, return_url, cancel_url):
    price = subscription.price
    quantity = "1"
    name = "Movify " + subscription.name + " subscription"
    description = subscription.description
    sku = _generate_product_name(subscription.months)
    payment_data = paypal_payment(price, quantity, name, description, sku, return_url, cancel_url)
    url = payment_data["url"]
    paypal_id = payment_data["id"]
    session[PAYPAL_ID_KEY] = _to_md5(paypal_id)
    return {"url": url}


def _get_cajastur_payment_data(subscription, return_url, cancel_url):
    operation = _generate_product_name(subscription.months)
    price = subscription.price
    description = subscription.name
    return cajastur_payment(operation, price, description, return_url, cancel_url)


@app.route(prefix + "/account/subscription/paypal")
@login_required
def proccess_paypal_payment():
    paypal_id = request.args.get("paymentId")
    paypal_id_hash = session[PAYPAL_ID_KEY]
    if paypal_id_hash == _to_md5(paypal_id):
        return "OK"
    else:
        return "FAIL"


# Movies

@app.route(prefix + "/movies", methods=["GET"])
@login_required
def show_movies():
    movies = movie_service.get_all()
    return dumps([movie.to_dict() for movie in movies])


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