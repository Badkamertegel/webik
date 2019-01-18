from cs50 import SQL
from flask import Flask, render_template, redirect, url_for, request
from helpers import *
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import os


app = Flask(__name__)

db = SQL("sqlite:///project.db")

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    return apology("TODO", 200)




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

        password = request.form.get("password")
        hash = pwd_context.hash(password)

        result = db.execute("INSERT INTO user2 (username, hash) VALUES (:username, :password)",
                            username=request.form.get("username"), password=hash)

        if not result:
            return apology("username is already in use")
        else:
            return apology("registration complete", 200)

        session["user_id"] = result

        return redirect(url_for("index"))
    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM user2 WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return "invalid username and/or password"

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/teacherlogin", methods=["GET","POST"])
def teacherlogin():

    session.clear()


    if request.method == "POST":


        if not request.form.get("username"):
            return apology("must provide username")


        elif not request.form.get("password"):
            return apology("must provide password")


        rows = db.execute("SELECT * FROM teachers WHERE username = :username", username=request.form.get("username"))


        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return "invalid username and/or password"


        session["user_id"] = rows[0]["id"]


        return redirect(url_for("index"))


    else:
        return render_template("login.html")

@app.route("/teacherRegister", methods=["GET","POST"])
def teacherRegister():
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must choose a username")

        elif not request.form.get("password"):
            return apology("must choose a password")

        elif not request.form.get("confirmation"):
            return apology("must fill in password again")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("both passwords must be the same")

        password = request.form.get("password")
        hash = pwd_context.hash(password)

        result = db.execute("INSERT INTO teachers (username, hash) VALUES (:username, :password)",
                            username=request.form.get("username"), password=hash)

        if not result:
            return apology("username is already in use")
        else:
            return apology("registration complete", 200)

        session["user_id"] = result

        return redirect(url_for("index"))
    else:
        return render_template("register.html")





