from functools import wraps
from flask import Flask, session
from flask import render_template, request, session, redirect, url_for
import json
from user import User
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



@app.route('/categories')
def get_categories():
    return render_template("categories.html", categories=Category.all())