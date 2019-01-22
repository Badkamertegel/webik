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

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

db = SQL("sqlite:///project.db")

data = Trivia(True)
response = data.request(1, Category.History ,Diffculty.Hard, Type.Multiple_Choice)
informatie = []

for info in response['results']:
    informatie.append(info)

categorie = []
vraag = []
goed_antwoord = []
foute_antwoorden = []
moeilijkheidsgraad = []

for element in range(len(informatie)):
    categorie.append(informatie[element]['category'])
    vraag.append(informatie[element]['question'])
    goed_antwoord.append(informatie[element]['correct_answer'])
    foute_antwoorden.append(informatie[element]['incorrect_answers'])
    moeilijkheidsgraad.append(informatie[element]['difficulty'])

print(foute_antwoorden[0][0])





@app.route("/create")
@login_required
def create():

    if request.method =="POST":

        teacher_value = db.execute("SELECT teacher FROM user WHERE username = :username", username=request.form.get("username"))

        if teacher_value == 1:
            session["user_id"] = user
        else:
            session["user_id"] = teacher

        return redirect(url_for("create.html"))


    else:
        # print(categorie)
        return render_template("create.html", category=categorie, vraag=vraag, goed=goed_antwoord, fout=foute_antwoorden, moeilijkheidsgraad=moeilijkheidsgraad)

@app.route("/game")
@login_required
def game():

    if request.method == "GET":

        counter = 0

        if request.form.get("goed"):
            counter += 1


        return render_template("game.html", categorie=categorie[0], vraag = vraag[0], moeilijkheidsgraad = moeilijkheidsgraad[0], goed = goed_antwoord[0], fout_1 = foute_antwoorden[0][0], fout_2 = foute_antwoorden[0][1], fout_3 = foute_antwoorden[0][2])


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

    return render_template("homepage.html")

@app.route("/result_student", methods=["GET","POST"])
@login_required
def result_student():

    return render_template("result_student.html", categorie = categorie, moeilijkheidsgraad = moeilijkheidsgraad, counter = counter)

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



