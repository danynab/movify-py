from datetime import datetime
from time import mktime

import hashlib
from application.model.user import User
from application.persistence import user_persistence


__author__ = 'Dani Meana'


def get(username):
    return user_persistence.get(username)


def get_all():
    return user_persistence.get_all()


def signup(username, password, email):
    user = get(username)
    if user is not None:
        return None
    password_hash = hashlib.md5(password.encode('utf')).hexdigest()
    today = datetime.now().date()
    today_millis = int(mktime(today.timetuple()) * 1000)
    print(today_millis)
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