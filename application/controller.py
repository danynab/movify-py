from datetime import datetime
from time import time

from application.payments.cajastur import cajastur_payment
from application.payments.paypal import paypal_payment
from flask.json import dumps
from functools import wraps
from application import app, prefix
from flask import redirect, request, render_template, url_for, session, g
from application.services import user_service, movie_service, review_service, subscription_service, genre_service
import hashlib
import random


__author__ = 'Dani Meana'

SESSION_ID_KEY = 'session_id'
USERNAME_KEY = 'username'
PAYPAL_ID_KEY = 'paypal_id'
CAJASTUR_ID_KEY = 'cajastur_id'
MONTHS_KEY = 'months'


def _to_md5(string):
    return hashlib.md5(string.encode('utf')).hexdigest()


def _calculate_session_id():
    ip = g.get('ip', '')
    user_agent = g.get('user_agent', '')
    session_id_str = ip + user_agent
    return _to_md5(_to_md5(session_id_str))


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


def _generate_product_name(months):
    date_now = datetime.now()
    date_now_str = str(date_now.year) + str(date_now.month) + str(date_now.day) + str(date_now.hour) + str(
        date_now.minute) + str(date_now.second)
    return 'Movify' + str(months) + 'm' + date_now_str


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


@app.route(prefix + '/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route(prefix + '/init')
def init():
    import application.data as data
    from application import db

    db.drop_all()
    db.create_all()

    user_dani = user_service.signup('dani', 'dani', 'dani@movify.es')
    user_david = user_service.signup('david', 'david', 'david@movify.es')
    user_marco = user_service.signup('marco', 'marco', 'marco@movify.es')

    for subscription in data.subscriptions:
        subscription_service.save(
            name=subscription['name'],
            description=subscription['description'],
            months=subscription['months'],
            price=subscription['price'])

    for genre in data.genres:
        genre_service.save(
            name=genre["name"],
            image='http://156.35.95.67/movify/static/genres/' + genre["image"]
        )

    for movie in data.movies:
        try:
            movie_url = 'http://156.35.95.67/movify/static/movies/' + movie['movie']
            trailer_url = 'http://156.35.95.67/movify/static/trailers/' + movie['trailer']
        except KeyError:
            movie_url = ''
            trailer_url = ''
        movie_saved = movie_service.save(
            title=movie['title'],
            year=movie['year'],
            duration=movie['duration'],
            genres=[genre_service.get(genre) for genre in movie['categories']],
            description=movie['description'],
            storyline=movie['storyline'],
            director=movie['director'],
            writers=movie['writers'],
            stars=movie['stars'],
            cover='http://156.35.95.67/movify/static/cov'
                  'ers/' + movie['cover'],
            background='http://156.35.95.67/movify/static/background/' + movie['background'],
            movie=movie_url,
            trailer=trailer_url
        )

        review_service.rate_movie(movie_saved, user_dani, random.randint(0, 10),
                                  'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque vitae metus in '
                                  'erat pellentesque tristique. Aliquam non tincidunt velit. Integer placerat luctus '
                                  'velit, vitae lacinia nisi placerat id. Duis at sapien nulla. Duis scelerisque quam '
                                  'et diam semper, a commodo libero rhoncus. Fusce bibendum id nibh eu rhoncus. Nulla '
                                  'cursus, libero at maximus aliquam, leo justo efficitur urna, ac elementum sem nunc '
                                  'eu tellus. Nullam fringilla porta venenatis. In pharetra quam pretium ex suscipit '
                                  'luctus. Sed ornare varius tortor, ac ornare tellus tristique et. Aenean vel '
                                  'ultrices tortor. Morbi tempus commodo quam nec ultrices. Vestibulum at enim magna. '
                                  'Vivamus auctor semper libero varius rutrum. Ut vel fringilla nisi.')

        review_service.rate_movie(movie_saved, user_david, random.randint(0, 10),
                                  'Proin congue tincidunt orci, fringilla maximus urna rutrum in. Duis elementum '
                                  'ultrices scelerisque. Praesent ante est, vestibulum in nulla vel, dignissim '
                                  'interdum nisl. Morbi ullamcorper odio porttitor, interdum lacus non, viverra mi. '
                                  'Ut ut congue libero. In fringilla orci ligula, mattis viverra lorem pulvinar sit '
                                  'amet. Vestibulum et mi massa.')
        review_service.rate_movie(movie_saved, user_marco, random.randint(0, 10),
                                  'Sed sit amet semper nisl. Proin eget lorem ut felis auctor rutrum in a lectus. '
                                  'Aenean eget lacinia elit. Nulla molestie risus a diam posuere, sit amet interdum '
                                  'ipsum tempor. Nunc ac vehicula sem. Ut tincidunt libero leo, a accumsan nulla '
                                  'iaculis ac. Nunc volutpat tempor justo et pellentesque. Aenean lorem metus, '
                                  'hendrerit at velit sed, euismod porttitor eros. Curabitur elementum felis mauris, '
                                  'in condimentum mauris placerat eget. Aliquam pellentesque ipsum quis consectetur '
                                  'aliquet.')

    return redirect(url_for('index'))


# Users

@app.route(prefix + '/login', methods=['GET'])
def show_login():
    return render_template('login.html')


@app.route(prefix + '/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = user_service.login(username, password)
    if user is not None:
        session_id = _calculate_session_id()
        print(SESSION_ID_KEY)
        session[SESSION_ID_KEY] = session_id
        session[USERNAME_KEY] = username
        return redirect(url_for('index'))
    else:
        return redirect(url_for('show_login'))


@app.route(prefix + '/logout', methods=['GET'])
@login_required
def do_logout():
    session.pop(SESSION_ID_KEY)
    session.pop(USERNAME_KEY)
    return redirect(url_for('index'))


@app.route(prefix + '/signup', methods=['GET'])
def show_signup():
    return render_template('signup.html')


@app.route(prefix + '/signup', methods=['POST'])
def do_signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    confirm_email = request.form['confirm_email']
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
            return redirect(url_for('index'))
        return "Username already registered"
    else:
        return "Emails not equals"


# Account

@app.route(prefix + '/account', methods=['GET'])
@login_required
def show_account():
    subscriptions = subscription_service.get_order_by_months()
    username = session[USERNAME_KEY]
    user = user_service.get(username)
    expiration = user.expiration
    expiration_date = datetime.fromtimestamp(expiration / 1000)
    expiration_date_str = expiration_date.strftime("%b %d, %Y")
    return render_template('account.html',
                           subscriptions=subscriptions,
                           user={"username": user.username,
                                 "expiration": user.expiration,
                                 "expiration_str": expiration_date_str},
                           today_millis=int(time() * 1000))


@app.route(prefix + '/_generate_cajastur_payment_data')
@login_required
def generate_cajastur_payment_data():
    months = request.args.get('months', 0, type=int)
    subscription = subscription_service.get_by_months(months)
    if subscription is None:
        return redirect(url_for('index'))
    else:
        return_url = 'http://156.35.95.67/movify/account/subscription/cajastur'
        cancel_url = 'http://156.35.95.67/movify/account'
        cajastur_data = _get_cajastur_payment_data(subscription, return_url, cancel_url)
        return dumps(cajastur_data)


@app.route(prefix + '/_generate_paypal_payment_data')
@login_required
def generate_paypal_payment_data():
    months = request.args.get('months', 0, type=int)
    subscription = subscription_service.get_by_months(months)
    if subscription is None:
        return redirect(url_for('index'))
    else:
        return_url = 'http://156.35.95.67/movify/account/subscription/paypal'
        cancel_url = 'http://156.35.95.67/movify/account'
        paypal_data = _get_paypal_payment_data(subscription, return_url, cancel_url)
        return dumps(paypal_data)


def _get_paypal_payment_data(subscription, return_url, cancel_url):
    price = subscription.price
    quantity = '1'
    name = 'Movify ' + subscription.name + ' subscription'
    description = subscription.description
    sku = _generate_product_name(subscription.months)
    payment_data = paypal_payment(price, quantity, name, description, sku, return_url, cancel_url)
    url = payment_data['url']
    paypal_id = payment_data['id']
    session[MONTHS_KEY] = subscription.months
    session[PAYPAL_ID_KEY] = _to_md5(paypal_id)
    return {'url': url}


def _get_cajastur_payment_data(subscription, return_url, cancel_url):
    operation = _generate_product_name(subscription.months)
    price = subscription.price
    description = 'Movify ' + subscription.name + ' subscription'
    payment_data = cajastur_payment(operation, price, description, return_url, cancel_url)
    session[MONTHS_KEY] = subscription.months
    session[CAJASTUR_ID_KEY] = _to_md5(payment_data["signature"])
    return payment_data


@app.route(prefix + '/account/subscription/paypal')
@login_required
def proccess_paypal_payment():
    paypal_id = request.args.get('paymentId')
    paypal_id_hash = session[PAYPAL_ID_KEY]
    months = session[MONTHS_KEY]
    session.pop(PAYPAL_ID_KEY)
    session.pop(MONTHS_KEY)
    username = session[USERNAME_KEY]
    if paypal_id_hash == _to_md5(paypal_id):
        user_service.increase_expiration(username, months)
        return redirect(url_for('show_account'))
    else:
        return 'FAIL'


@app.route(prefix + '/account/subscription/cajastur')
@login_required
def proccess_cajastur_payment():
    cajastur_id = session[CAJASTUR_ID_KEY]
    months = session[MONTHS_KEY]
    session.pop(MONTHS_KEY)
    username = session[USERNAME_KEY]
    if cajastur_id is not None:
        user_service.increase_expiration(username, months)
    return redirect(url_for('show_account'))


# Movies

@app.route(prefix + '/movies', methods=['GET'])
# @login_required
def find_movies():
    title = request.args.get('title')
    if title is None:
        movies = movie_service.get_all()
    else:
        movies = movie_service.find_by_title(title)
    return dumps(movie_service.movies_to_dicts(movies))


@app.route(prefix + '/movies/<int:movie_id>', methods=['GET'])
# @login_required
def get_movie(movie_id):
    movie = movie_service.get(movie_id)
    return dumps(movie_service.movie_to_dict(movie))


@app.route(prefix + '/movies/<int:movie_id>/rates', methods=['POST'])
@login_required
def rate_movie(movie_id):
    value = request.form['value']
    users = user_service.get_all()
    user = users[users.__len__() - 1]
    rate = review_service.rate_movie(movie_id, user.username, value)
    return redirect(url_for('show_movies'))


# Genres

@app.route(prefix + '/genres', methods=["GET"])
# @login_required
def find_genres():
    genres = genre_service.get_all()
    return dumps(genre_service.genres_to_dicts(genres, add_movies=False))


@app.route(prefix + '/genres/<genre_name>', methods=["GET"])
# @login_required
def get_genre(genre_name):
    genre = genre_service.get(genre_name)
    return dumps(genre_service.genre_to_dict(genre))


@app.route(prefix + '/genres/<genre_name>/movies', methods=['GET'])
# @login_required
def find_movies_by_genre(genre_name):
    movies = genre_service.get_movies(genre_name)
    return dumps(movie_service.movies_to_dicts(movies))


# UTIL

@app.route(prefix + '/util', methods=['GET'])
@login_required
def show_util():
    movies = movie_service.get_all()
    return render_template('util.html', movies=movies)
