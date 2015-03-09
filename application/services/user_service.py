import hashlib
from application.model.user import User
from application.persistence import user_persistence

__author__ = 'Dani Meana'


def get(username):
    return user_persistence.get(username)


def register(username, password, email, first_name, last_name):
    user = get(username)
    if user is not None:
        return None
    password_hash = hashlib.md5(password.encode("utf")).hexdigest()
    user = User(username, password_hash, email, first_name, last_name)
    user_persistence.save(user)
    return user


def login(username, password):
    user = get(username)
    if user is None:
        return None
    password_hash = hashlib.md5(password.encode("utf")).hexdigest()
    if user.password == password_hash:
        return user
    return None