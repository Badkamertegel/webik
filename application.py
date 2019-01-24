# https://github.com/MaT1g3R/Python-Trivia-API

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from helpers import *
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import aiohttp, requests
import urllib.request
import json
import os
from pytrivia import Category, Diffculty, Type, Trivia
from enum import Enum

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

db = SQL("sqlite:///project.db")

category = ["general", "geography", "history", "film", "nature", "music"]
difficulty = ["easy", "medium", "hard"]
data = Trivia(True)

quiz_namen = db.execute("SELECT quiz FROM maken")
print(quiz_namen[0]["quiz"])

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":

        db.execute("INSERT INTO maken (quiz, category, difficulty, questions) VALUES (:quiz, :category, :difficulty, :questions)", quiz = request.form.get("quiz_name"), category = request.form.get("categorie"), difficulty = request.form.get("difficulty"), questions = request.form.get("questions"))
        return redirect(url_for("game"))

    else:
        return render_template("create.html", categorie = category, difficulty = difficulty)

@app.route("/game", methods=["GET", "POST"])
@login_required
def game():

    if request.method == "GET":

        category = db.execute("SELECT category FROM maken")[2]["category"]
        difficulty = db.execute("SELECT difficulty FROM maken")[2]["difficulty"]
        questions = db.execute("SELECT questions FROM maken")[2]["questions"]

        dict_api = {'general': 9, 'geography': 22, 'history': 23, 'film': 11, 'nature': 17, 'music': 12}
        dict_api_difficulty = {'hard': 'hard', 'medium': 'medium', 'easy': 'easy'}
        x = dict_api[category]
        y = dict_api_difficulty[difficulty]
        main_api = "https://opentdb.com/api.php?"
        url = main_api + urllib.parse.urlencode({'amount': questions}) +"&"+ urllib.parse.urlencode({'category': x}) +"&"+ urllib.parse.urlencode({'difficulty': y}) +"&"+ urllib.parse.urlencode({'type': 'multiple'})
        api_data = requests.get(url).json()['results']

        return render_template("game.html", api_data = api_data)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must choose a username")

        elif not request.form.get("password"):
            return apology("must choose a password")

        elif not request.form.get("confirmation"):
            return apology("must fill in password again")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("both passwords must be the same")

        if request.form.get("checkbox"):
            teacher = 1
        else:
            teacher = 0


        result = db.execute("INSERT INTO user (username, hash, teacher) VALUES (:username, :hash, :teacher)",
                            username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")), teacher = teacher)

        if not result:
            return apology("username is already in use")

        session["user_id"] = result

        return redirect(url_for("homepage"))
    else:
        return render_template("register.html")



@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

     #ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

         # query database for username
        rows = db.execute("SELECT * FROM user WHERE username = :username", username=request.form.get("username"))

         # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
             return "invalid username and/or password and/or teacher"


         # remember which user has logged in
        session["user_id"] = rows[0]["id"]


        # redirect user to home page
        return redirect(url_for("homepage"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/homepage", methods=["GET","POST"])
@login_required
def homepage():

    if request.method == "POST":

        quiz_namen = db.execute("SELECT quiz FROM maken")

        if request.form.get("join") == quiz_namen[0]["quiz"]:
            return redirect(url_for("game"))
        else:
            return redirect(url_for("homepage"))

    else:
        return render_template("homepage.html")

@app.route("/result_student", methods=["GET","POST"])
@login_required
def result_student():

    return render_template("result_student.html",)

@app.route("/result_teacher", methods=["GET","POST"])
@login_required
def result_teacher():
    if request.method == "POST":

        return render_template("result_teacher.html")

@app.route("/logout")
def logout():

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))