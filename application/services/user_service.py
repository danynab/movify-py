from datetime import datetime
from time import mktime

from application import db
from dateutil.relativedelta import relativedelta

import hashlib
from application.model.user import User
from application.persistence import user_persistence


__author__ = 'Dani Meana'


def get(username):
    return user_persistence.get(username)


def get_all():
    return user_persistence.get_all()


def increase_expiration(username, months):
    user = get(username)
    expiration = user.expiration
    expiration_date = datetime.fromtimestamp(expiration / 1000)
    new_expiration_date = expiration_date + relativedelta(months=months)
    new_expiration = int(mktime(new_expiration_date.timetuple()) * 1000)
    user.expiration = new_expiration
    db.session.merge(user)
    db.session.commit()


def signup(username, password, email):
    user = get(username)
    if user is not None:
        return None
    password_hash = hashlib.md5(password.encode('utf')).hexdigest()
    today = datetime.now().date()
    today_millis = int(mktime(today.timetuple()) * 1000)
    user = User(username, password_hash, email, today_millis)
    user_persistence.save(user)
    return user


def login(username, password):
    user = get(username)
    if user is None:
        return None
    password_hash = hashlib.md5(password.encode('utf')).hexdigest()
    if user.password == password_hash:
        return user
    return None