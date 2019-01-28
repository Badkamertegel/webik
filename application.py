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
import random
from random import shuffle

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

db = SQL("sqlite:///project.db")

category = ["general", "geography", "history", "film", "nature", "music"]
difficulty = ["easy", "medium", "hard"]
data = Trivia(True)

a = db.execute("SELECT quiz, quiz_id FROM game")
lijst = []
for b in a:
    tijdelijk = []
    tijdelijk.append(b['quiz'])
    tijdelijk.append(b['quiz_id'])
    lijst.append(tijdelijk)
print(lijst)

lijst_2 = []
cate = db.execute("SELECT category FROM game")
for categ in cate:
    lijst_2.append(categ['category'])
print(lijst_2)

quiz_id = db.execute("SELECT quiz_id FROM game")
lijst_3 = []
for idd in quiz_id:
    lijst_3.append(idd['quiz_id'])
print(lijst_3)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":

        cat = request.form.get("categorie")
        dif = request.form.get("difficulty")
        quiz = request.form.get("quiz_name")
        questions = request.form.get("questions")

        db.execute("INSERT INTO game (quiz, category, difficulty, questions, vragen_count) VALUES (:quiz, :cat, :dif, :questions, '1')",
                                quiz = quiz, cat = cat, dif = dif, questions = questions)

        return redirect(url_for("homepage"))

    else:
        return render_template("create.html", categorie = category, difficulty = difficulty)

@app.route("/game", methods=["GET", "POST"])
@login_required
def game():

    print(request.method)
    if request.method == "POST":

        if str(request.form["button"]).strip() == str(request.form["answer"]).strip():
            db.execute("UPDATE user SET counter = counter + 1 WHERE id = :id", id=session["user_id"])
        if request.form.get("button"):
            db.execute("UPDATE game SET vragen_count = vragen_count + 1")

        vragen_count = db.execute("SELECT vragen_count FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['vragen_count']
        cate = db.execute("SELECT category FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["category"]
        diffi = db.execute("SELECT difficulty FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["difficulty"]
        aantal_questions = db.execute("SELECT questions FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["questions"]

        dict_api = {'general': 9, 'geography': 22, 'history': 23, 'film': 11, 'nature': 17, 'music': 12}
        dict_api_difficulty = {'hard': 'hard', 'medium': 'medium', 'easy': 'easy'}
        x = dict_api[cate]
        y = dict_api_difficulty[diffi]

        main_api = "https://opentdb.com/api.php?"
        url = main_api + urllib.parse.urlencode({'amount': aantal_questions}) +"&"+ urllib.parse.urlencode({'category': x}) +"&"+ urllib.parse.urlencode({'difficulty': y}) +"&"+ urllib.parse.urlencode({'type': 'multiple'})
        api_data = requests.get(url).json()['results']

        mogelijkheden = []

        for i in api_data:

            vraag = api_data[0]['question']
            goed = api_data[0]['correct_answer']
            fout_1 = api_data[0]['incorrect_answers'][0]
            fout_2 = api_data[0]['incorrect_answers'][1]
            fout_3 = api_data[0]['incorrect_answers'][2]

            mogelijkheden.append((goed, fout_1, fout_2, fout_3))

        mogelijkheid = list(mogelijkheden[0])
        random.shuffle(mogelijkheid)

        if vragen_count > aantal_questions:
            return redirect(url_for("result_student"))
        else:
            return render_template("game.html", api_data = api_data, vraag = vraag, a=mogelijkheid[0], b=mogelijkheid[1], c=mogelijkheid[2], d=mogelijkheid[3], goed= goed, count=vragen_count)

    else:

        vragen_count = db.execute("SELECT vragen_count FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['vragen_count']
        cate = db.execute("SELECT category FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["category"]
        diffi = db.execute("SELECT difficulty FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["difficulty"]
        aantal_questions = db.execute("SELECT questions FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["questions"]

        dict_api = {'general': 9, 'geography': 22, 'history': 23, 'film': 11, 'nature': 17, 'music': 12}
        dict_api_difficulty = {'hard': 'hard', 'medium': 'medium', 'easy': 'easy'}
        x = dict_api[cate]
        y = dict_api_difficulty[diffi]

        main_api = "https://opentdb.com/api.php?"
        url = main_api + urllib.parse.urlencode({'amount': aantal_questions}) +"&"+ urllib.parse.urlencode({'category': x}) +"&"+ urllib.parse.urlencode({'difficulty': y}) +"&"+ urllib.parse.urlencode({'type': 'multiple'})
        api_data = requests.get(url).json()['results']

        mogelijkheden = []

        for i in api_data:

            vraag = api_data[0]['question']
            goed = api_data[0]['correct_answer']
            fout_1 = api_data[0]['incorrect_answers'][0]
            fout_2 = api_data[0]['incorrect_answers'][1]
            fout_3 = api_data[0]['incorrect_answers'][2]

            mogelijkheden.append((goed, fout_1, fout_2, fout_3))

        mogelijkheid = list(mogelijkheden[0])
        random.shuffle(mogelijkheid)

        return render_template("game.html", api_data = api_data, vraag = vraag, a=mogelijkheid[0], b=mogelijkheid[1], c=mogelijkheid[2], d=mogelijkheid[3], goed= goed, count=vragen_count)

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


        result = db.execute("INSERT INTO user (username, hash, teacher, counter) VALUES (:username, :hash, :teacher, 0)",
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

        quiz_namen = db.execute("SELECT quiz, quiz_id FROM game")
        quiz_namen_lijst = []
        for quiz_naam in quiz_namen:
            quiz_namen_lijst.append(quiz_naam['quiz'])

        if request.form.get("join") in quiz_namen_lijst:
            db.execute("UPDATE user SET counter = 0 WHERE id = :id", id=session["user_id"])
            db.execute("UPDATE game SET vragen_count = 1 WHERE quiz=:quiz", quiz = request.form.get("join"))
            session['game'] = request.form.get("join")
            return redirect(url_for("game"))
        else:
            return redirect(url_for("homepage"))

    else:
        return render_template("homepage.html")

@app.route("/result_student", methods=["GET","POST"])
@login_required
def result_student():

    result_category = db.execute("SELECT category FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['category']
    result_difficulty= db.execute("SELECT difficulty FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['difficulty']
    result_score = db.execute("SELECT counter FROM user WHERE id=:id", id=session['user_id'])[0]['counter']
    result_total = db.execute("SELECT questions FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['questions']
    gebruiker = db.execute("SELECT username FROM user WHERE id=:id", id= session['user_id'])[0]['username']

    return render_template("result_student.html", username=gebruiker, quiz=session['game'], result_category=result_category, result_difficulty=result_difficulty, result_score=result_score, result_total=result_total)

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