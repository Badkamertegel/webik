import csv
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def encrypt(text):

    cypher = ""
    for j in range(len(text)):
        i = chr(ord(text[j]) + 3)
        cypher = cypher + i
    return cypher

def omzetten(input):

    input = input.replace('&quot;', "'").replace('&#039;', "'").replace('&shy;', '').replace('&aring;','å').replace('&rsquo;', "'").replace('&eacute;', "é").replace('&ldquo;', "'").replace('&rdquo;', "'").replace('&deg;', "°").replace('&hellip;', "...").replace('&amp;', "&")

    return input

