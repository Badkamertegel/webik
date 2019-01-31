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
import time

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

db = SQL("sqlite:///project.db")

# Lists with categories and difficulties for create.html
category = ["general", "geography", "history", "film", "nature", "music"]
difficulty = ["easy", "medium", "hard"]
data = Trivia(True)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":

        # Get input from create.html
        cat = request.form.get("categorie")
        dif = request.form.get("difficulty")
        quiz = request.form.get("quiz_name")
        questions = request.form.get("questions")

        # Creator of the quiz
        gebruikersnaam = db.execute("SELECT username FROM user WHERE id=:id", id= session['user_id'])[0]['username']
        session['username'] = gebruikersnaam

        # Check if the quiz name is unique
        bestaande_quizen = []
        bestaande_quiz = db.execute("SELECT quiz FROM game")
        for bestaande_quiz_index in bestaande_quiz:
            bestaande_quizen.append(bestaande_quiz_index['quiz'])

        if quiz in bestaande_quizen:
            return render_template("create.html", categorie = category, difficulty = difficulty)
        else:

            # Insert quiz into database
            db.execute("INSERT INTO game (quiz, category, difficulty, questions, vragen_count, creator) VALUES (:quiz, :cat, :dif, :questions, '1', :creator)",
                                quiz = quiz, cat = cat, dif = dif, questions = questions, creator = session['username'])

        return redirect(url_for("homepage"))

    else:
        return render_template("create.html", categorie = category, difficulty = difficulty)

@app.route("/game", methods=["GET", "POST"])
@login_required
def game():

    print(request.method)
    if request.method == "POST":

        # Check given is equal to the correct answer
        if encrypt(request.form["button"]) == request.form["answer"].strip():
            db.execute("UPDATE user SET counter = counter + 1 WHERE id = :id", id=session["user_id"])

        # Keeps track of the current question
        if request.form.get("button"):
            db.execute("UPDATE game SET vragen_count = vragen_count + 1")

        # These variables are needed to generate a question
        vragen_count = db.execute("SELECT vragen_count FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['vragen_count']
        cate = db.execute("SELECT category FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["category"]
        diffi = db.execute("SELECT difficulty FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["difficulty"]
        aantal_questions = db.execute("SELECT questions FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["questions"]

        # Convert variables to the right template
        dict_api = {'general': 9, 'geography': 22, 'history': 23, 'film': 11, 'nature': 17, 'music': 12}
        dict_api_difficulty = {'hard': 'hard', 'medium': 'medium', 'easy': 'easy'}
        x = dict_api[cate]
        y = dict_api_difficulty[diffi]

        # Questions are getting extracted from the API
        main_api = "https://opentdb.com/api.php?"
        url = main_api + urllib.parse.urlencode({'amount': aantal_questions}) +"&"+ urllib.parse.urlencode({'category': x}) +"&"+ urllib.parse.urlencode({'difficulty': y}) +"&"+ urllib.parse.urlencode({'type': 'multiple'})
        api_data = requests.get(url).json()['results']

        mogelijkheden = []

        for i in api_data:

            # Call the correct and incorrect answers
            vraag = omzetten(api_data[0]['question'])
            goed = omzetten(api_data[0]['correct_answer'])
            goed_hash = omzetten(encrypt(goed))
            fout_1 = omzetten(api_data[0]['incorrect_answers'][0])
            fout_2 = omzetten(api_data[0]['incorrect_answers'][1])
            fout_3 = omzetten(api_data[0]['incorrect_answers'][2])

            mogelijkheden.append((goed, fout_1, fout_2, fout_3))

        # Answers are shuffled
        mogelijkheid = list(mogelijkheden[0])
        random.shuffle(mogelijkheid)

        if vragen_count > aantal_questions:
            return redirect(url_for("result_student"))
        else:
            return render_template("game.html", api_data = api_data, vraag = vraag, a=mogelijkheid[0], b=mogelijkheid[1], c=mogelijkheid[2], d=mogelijkheid[3], goed= goed_hash, count=vragen_count)

    else:

        # These variables are needed to generate a question
        vragen_count = db.execute("SELECT vragen_count FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['vragen_count']
        cate = db.execute("SELECT category FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["category"]
        diffi = db.execute("SELECT difficulty FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["difficulty"]
        aantal_questions = db.execute("SELECT questions FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]["questions"]

        # Convert variables to the right template
        dict_api = {'general': 9, 'geography': 22, 'history': 23, 'film': 11, 'nature': 17, 'music': 12}
        dict_api_difficulty = {'hard': 'hard', 'medium': 'medium', 'easy': 'easy'}
        x = dict_api[cate]
        y = dict_api_difficulty[diffi]

        # Questions are getting extracted from the API
        main_api = "https://opentdb.com/api.php?"
        url = main_api + urllib.parse.urlencode({'amount': aantal_questions}) +"&"+ urllib.parse.urlencode({'category': x}) +"&"+ urllib.parse.urlencode({'difficulty': y}) +"&"+ urllib.parse.urlencode({'type': 'multiple'})
        api_data = requests.get(url).json()['results']

        mogelijkheden = []

        for i in api_data:

            #Call the correct and incorrect answers
            vraag = omzetten(api_data[0]['question'])
            goed = omzetten(api_data[0]['correct_answer'])
            goed_hash = omzetten(encrypt(goed ))
            fout_1 = omzetten(api_data[0]['incorrect_answers'][0])
            fout_2 = omzetten(api_data[0]['incorrect_answers'][1])
            fout_3 = omzetten(api_data[0]['incorrect_answers'][2])

            mogelijkheden.append((goed, fout_1, fout_2, fout_3))

        # Answers are shuffled
        mogelijkheid = list(mogelijkheden[0])
        random.shuffle(mogelijkheid)

        return render_template("game.html", api_data = api_data, vraag = vraag, a=mogelijkheid[0], b=mogelijkheid[1], c=mogelijkheid[2], d=mogelijkheid[3], goed= goed_hash, count=vragen_count)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        # Must provide username
        if not request.form.get("username"):
            return render_template("register.html")

        # Must provide password
        elif not request.form.get("password"):
            return render_template("register.html")

        # Has to confirm password
        elif not request.form.get("confirmation"):
            return render_template("register.html")

        # Checks if the password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html")

        teacher = 0

        # Checks if username is unique
        db_usernames = db.execute("SELECT username FROM user")
        db_usernames_lijst= []
        for user in db_usernames:
            db_usernames_lijst.append(user['username'])

        if request.form.get("username") in db_usernames_lijst:
            return render_template("register.html")
        else:

            # Inserts student into database
            result = db.execute("INSERT INTO user (username, hash, teacher, counter) VALUES (:username, :hash, :teacher, 0)",
                            username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")), teacher = teacher)

        session["user_id"] = result

        return redirect(url_for("homepage"))
    else:
        return render_template("register.html")

@app.route("/teacher_register", methods=["GET", "POST"])
def teacher_register():

    if request.method == "POST":

        # Must provide username
        if not request.form.get("username"):
            return render_template("teacher_register.html")

        # Must provide password
        elif not request.form.get("password"):
            return render_template("teacher_register.html")

        # Has to confirm password
        elif not request.form.get("confirmation"):
            return render_template("teacher_register.html")

        # Checks if the password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("teacher_register.html")

        teacher = 1

        # Checks if username is unique
        db_usernames = db.execute("SELECT username FROM user")
        db_usernames_lijst= []
        for user in db_usernames:
            db_usernames_lijst.append(user['username'])

        if request.form.get("username") in db_usernames_lijst:
            return render_template("register.html")
        else:

            # Inserts teacher into database
            result = db.execute("INSERT INTO user (username, hash, teacher, counter) VALUES (:username, :hash, :teacher, 0)",
                            username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")), teacher = teacher)

        session["user_id"] = result

        return redirect(url_for("homepage"))
    else:
        return render_template("teacher_register.html")


@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    if request.method == "POST":

     # Must provide existing username
        if not request.form.get("username"):
            return render_template("login.html")

        # Must provide correct password
        elif not request.form.get("password"):
            return render_template("login.html")

         # Select user from database
        rows = db.execute("SELECT * FROM user WHERE username = :username", username=request.form.get("username"))

         # Checks if username and password are correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
             return render_template("login.html")

         #Link user to session
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect(url_for("homepage"))

    else:
        return render_template("login.html")

@app.route("/homepage", methods=["GET","POST"])
@login_required
def homepage():

    if request.method == "POST":

        # Checks if quiz is unique
        quiz_namen = db.execute("SELECT quiz FROM game")
        quiz_namen_lijst = []
        for quiz_naam in quiz_namen:
            quiz_namen_lijst.append(quiz_naam['quiz'])

        # Checks if input equals a existing quiz
        if request.form.get("join") in quiz_namen_lijst:

            # Resets counter and updates vragen_count
            db.execute("UPDATE user SET counter = 0 WHERE id = :id", id=session["user_id"])
            db.execute("UPDATE game SET vragen_count = 1 WHERE quiz=:quiz", quiz = request.form.get("join"))

            # Links game to session
            session['game'] = request.form.get("join")
            return redirect(url_for("game"))
        else:
            return redirect(url_for("homepage"))

    else:
        return render_template("homepage.html")

@app.route("/result_student", methods=["GET","POST"])
@login_required
def result_student():

    if request.method == "GET":

        # Extracts all information needed from database
        result_category = db.execute("SELECT category FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['category']
        result_difficulty= db.execute("SELECT difficulty FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['difficulty']
        result_score = db.execute("SELECT counter FROM user WHERE id=:id", id=session['user_id'])[0]['counter']
        result_total = db.execute("SELECT questions FROM game WHERE quiz = :quiz_name", quiz_name = session['game'])[0]['questions']
        gebruiker = db.execute("SELECT username FROM user WHERE id=:id", id= session['user_id'])[0]['username']
        timestamp = time.gmtime()
        timestamp_readable = time.strftime('%Y-%m-%d %H:%M:%S', timestamp)
        toevoegen_result = db.execute("INSERT INTO results (student, quiz, score, tijd) VALUES (:student, :quiz, :score, :tijd)", student=gebruiker, quiz=session['game'], score=result_score, tijd=timestamp_readable)

        return render_template("result_student.html", username=gebruiker, quiz=session['game'], result_category=result_category, result_difficulty=result_difficulty, result_score=result_score, result_total=result_total)
    else:

        return render_template("result_student.html")

@app.route("/result", methods=["GET","POST"])
@login_required
def result():

    if request.method == "POST":

        # Checks if user is a teacher or not
        teacher_id = db.execute("SELECT teacher FROM user where id=:id", id=session['user_id'])[0]['teacher']

        if teacher_id == 1:

            # Extracts information from database needed for the teachers results
            gebruiker = db.execute("SELECT username FROM user WHERE id=:id", id=session['user_id'])[0]['username']
            categorie_result = db.execute("SELECT category FROM game WHERE creator=:creator and quiz=:quiz_name", creator=gebruiker, quiz_name=request.form.get("quiz_result"))[0]['category']
            difficulty_result = db.execute("SELECT difficulty FROM game WHERE creator=:creator and quiz=:quiz_name", creator=gebruiker, quiz_name=request.form.get("quiz_result"))[0]['difficulty']
            questions_result = db.execute("SELECT questions FROM game WHERE creator=:creator and quiz=:quiz_name", creator=gebruiker, quiz_name=request.form.get("quiz_result"))[0]['questions']
            results = db.execute("SELECT student, score, tijd FROM results WHERE quiz=:quiz_name", quiz_name = request.form.get("quiz_result"))
            name_result = request.form.get("quiz_result")
            quizes = db.execute("SELECT quiz FROM game WHERE creator=:creator", creator=gebruiker)

            opties = []

            # Shows same quizes only once and adds them to list
            for quiz in quizes:
                if quiz['quiz'] in opties:
                    opties = opties
                else:
                    opties.append(quiz['quiz'])

            return render_template("result.html", results=results, quizes=opties, questions_result = questions_result, difficulty_result = difficulty_result, categorie_result = categorie_result, name_result = name_result)

        else:

            # Extracts information from database needed for the student results
            gebruiker = db.execute("SELECT username FROM user WHERE id=:id", id=session['user_id'])[0]['username']
            categorie_result = db.execute("SELECT category FROM game WHERE quiz=:quiz_name", quiz_name=request.form.get("quiz_result"))[0]['category']
            difficulty_result = db.execute("SELECT difficulty FROM game WHERE quiz=:quiz_name", quiz_name=request.form.get("quiz_result"))[0]['difficulty']
            questions_result = db.execute("SELECT questions FROM game WHERE quiz=:quiz_name", quiz_name=request.form.get("quiz_result"))[0]['questions']
            results = db.execute("SELECT student, score, tijd FROM results WHERE quiz=:quiz_name and student=:student", student = gebruiker, quiz_name = request.form.get("quiz_result"))
            name_result = request.form.get("quiz_result")
            quizes = db.execute("SELECT quiz FROM results WHERE student=:student", student=gebruiker)

            opties = []

            # Show same quizes only once and adds them to list
            for quiz in quizes:
                if quiz['quiz'] in opties:
                    opties = opties
                else:
                    opties.append(quiz['quiz'])

            return render_template("result.html", results=results, quizes=opties, questions_result = questions_result, difficulty_result = difficulty_result, categorie_result = categorie_result, name_result = name_result)

    else:

        # Checks if user is teacher
        teacher_id = db.execute("SELECT teacher FROM user WHERE id=:id", id=session['user_id'])[0]['teacher']

        if teacher_id is 1:

            # Loads quizes from database created by the teacher
            gebruiker = db.execute("SELECT username FROM user WHERE id=:id", id= session['user_id'])[0]['username']
            quizes = db.execute("SELECT quiz FROM game WHERE creator=:creator", creator=gebruiker)

            opties = []

            # Adds every quiz to list
            for quiz in quizes:
                opties.append(quiz['quiz'])

        else:

            # Loads quizes from database made by the students
            gebruiker = db.execute("SELECT username FROM user WHERE id=:id", id= session['user_id'])[0]['username']
            quizes = db.execute("SELECT quiz FROM results WHERE student=:student", student=gebruiker)

            opties = []

            # Shows same quizes only once and adds them to list
            for quiz in quizes:
                if quiz['quiz'] in opties:
                    opties = opties
                else:
                    opties.append(quiz['quiz'])

        return render_template("result.html", quizes = opties)

@app.route("/logout")
def logout():

    # Forgets session id
    session.clear()

    # Redirect to login page
    return redirect(url_for("login"))