from functools import wraps
from flask import Flask, session
from database import DB
from flask import render_template, request, session, redirect, url_for
import json
from user import User
from rating import Rating
from game import Game
from game_categories import Category
app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect('/login')
        return func(*args, **kwargs)

    return wrapper


def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = User.find_by_username(session["USERNAME"])
        if not user.admin:
            return redirect('/')
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
def hello_world():
    return redirect("/main")


@app.route("/login", methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            print("Wrong username or password")
            return redirect(request.url)

        else:
            session["logged_in"] = True
            session["USERNAME"] = username
            return redirect('/')

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        user = User.find_by_username(request.form['username'])
        if not user:
            values = (
                None,
                request.form['username'],
                User.hash_password(request.form['password']),
                0
            )
            User(*values).create()
            return redirect('/')
        else:
            return redirect(request.url)


@app.route('/games/sort_by_rating')
def sort_by_rating():
    return render_template("games.html", games=Game.sort_by_rating())


@app.route('/games/sort_by_alp')
def sort_by_alp():
    return render_template("games.html", games=Game.sort_by_alp())

@app.route('/games/newest')
def sort_by_newest():
    return render_template("games.html", games=Game.sort_by_newest())


@app.route('/main')
def main_page():
    return render_template("main.html")


@app.route('/profile')
@require_login
def view_profile():

    user = User.find_by_username(session["USERNAME"])

    if user.admin == 0:
        return render_template("user_profile.html", user = user)
    else:
        return render_template("user_profile_admin.html", user = user)


@app.route('/logout')
def sign_out():

    session["USERNAME"] = None
    session["logged_in"] = False
    return redirect('/')


@app.route('/games/<int:id>/rate', methods=["POST"])
@require_login
def rate_game(id):
    p = request.form["rating"]
    print p

    game = Game.find(id)
    print game.id
    user = User.find_by_username(session["USERNAME"])
    print user
    values = (
        None,
        request.form["rating"],
        user,
        game
    )
    Rating(*values).create()

    return redirect('/')


@app.route('/categories/<int:id>/delete')
@require_admin
def delete_category(id):
    Category.find(id).delete()
    return redirect("/")


@app.route('/categories/new', methods=["GET", "POST"])
@require_admin
def new_category():
    if request.method == "GET":
        return render_template("new_category.html")
    elif request.method == "POST":
        category = Category(None, request.form["name"])
        category.create()
        return redirect("/categories")


@app.route('/categories/<int:id>')
def get_category(id):
    return render_template("category.html", category=Category.find(id))


@app.route('/categories')
def get_categories():
    return render_template("categories.html", categories=Category.all())


@app.route('/games')
def list_games():
    return render_template('games.html', games=Game.all())


@app.route('/games/<int:id>')
def show_game(id):
    game = Game.find(id)
    rating = Game.calc_rating(id)
    return render_template('game.html', game=game, rating=rating)
