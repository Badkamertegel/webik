# https://github.com/MaT1g3R/Python-Trivia-API

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import aiohttp, requests
import urllib.request
import json
from pytrivia import Category, Diffculty, Type, Trivia

app = Flask(__name__)

data = Trivia(True)
response = data.request(2, Category.History ,Diffculty.Hard, Type.Multiple_Choice)
informatie = []

for info in response['results']:
    informatie.append(info)

for element in range(len(informatie)):
    categorie = informatie[element]['category']
    vraag = informatie[element]['question']
    goed_antwoord = informatie[element]['correct_answer']
    foute_antwoorden = informatie[element]['incorrect_answers']
    moeilijkheidsgraad = informatie[element]['difficulty']

print(categorie, vraag, goed_antwoord, foute_antwoorden, moeilijkheidsgraad)


@app.route("/index")
def index():

    categories = ['Maths', 'History']

    if request.method =="POST":

        return redirect(url_for("create.html"))

    else:
        # print(categorie)
        return render_template("index.html", category=categorie, vraag=vraag, goed=goed_antwoord, fout=foute_antwoorden, moeilijkheidsgraad=moeilijkheidsgraad)