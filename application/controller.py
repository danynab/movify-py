from application import app
from flask import redirect, request

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


@app.route("/", methods=["GET"])
def hello():
    return redirect("https://github.com/danynab/movify-py")