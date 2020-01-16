from functools import wraps
from flask import Flask, session
from flask import render_template, request, session, redirect, url_for
import json
from user import User
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
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
            0
        )
        User(*values).create()

        return redirect('/')

@app.route('/main')
def main_page():
    return render_template("main.html")

@app.route('/profile')
@require_login
def view_profile():
	
	user = User.find_by_username(session['USERNAME'])

	if user.admin == 0:
		return render_template("user_profile.html")
	else:
		return render_template("user_profile_admin.html")
@app.route('/logout')
def sign_out():

    session["USERNAME"] = None

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

if __name__ == "main":
    app.run(debug = True)